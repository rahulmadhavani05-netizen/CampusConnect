import streamlit as st
from sqlmodel import SQLModel, Field, create_engine, Session, select
from passlib.context import CryptContext
import enum, uuid
from datetime import datetime, date
import os

# ---------------- CONFIG ----------------
DB_FILE = "campus_connect.db"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------- ENUMS ----------------
class Role(str, enum.Enum):
    student = "student"
    placementCell = "placementCell"
    facultyMentor = "facultyMentor"
    employer = "employer"

class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    approved = "approved"
    rejected = "rejected"

# ---------------- MODELS ----------------
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    role: Role
    department: str | None = None
    hashed_password: str
    # preferences
    location_pref: str | None = None
    min_stipend_pref: int | None = None
    max_stipend_pref: int | None = None
    placement_conversion_pref: bool | None = False
    skills: str | None = None  # comma-separated skills

class Opportunity(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uid: str = Field(default_factory=lambda: f"opp-{uuid.uuid4().hex[:8]}")
    title: str
    company: str
    description: str
    required_skills: str
    department: str
    stipend: int
    duration: str
    location: str
    placement_conversion: bool = False
    application_deadline: date | None = None
    posted_by: int | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Application(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uid: str = Field(default_factory=lambda: f"app-{uuid.uuid4().hex[:8]}")
    student_id: int
    opportunity_id: int
    status: ApplicationStatus = ApplicationStatus.applied
    mentor_status: str | None = "pending"
    mentor_comments: str | None = None
    applied_date: datetime = Field(default_factory=datetime.utcnow)

# ---------------- DB INIT ----------------
def create_db_and_seed():
    if not os.path.exists(DB_FILE):
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            u1 = User(
                name="Rajesh Kumar", email="student@example.com", role=Role.student,
                department="Computer Science", hashed_password=pwd_context.hash("123"),
                skills="Python,React,SQL"
            )
            u2 = User(
                name="Placement Cell", email="placement@example.com", role=Role.placementCell,
                hashed_password=pwd_context.hash("123")
            )
            u3 = User(
                name="Faculty Mentor", email="mentor@example.com", role=Role.facultyMentor,
                hashed_password=pwd_context.hash("123")
            )
            u4 = User(
                name="Employer Inc", email="employer@example.com", role=Role.employer,
                hashed_password=pwd_context.hash("123")
            )
            session.add_all([u1, u2, u3, u4])
            session.commit()

            opp = Opportunity(
                title="Frontend Developer Intern", company="Tech Solutions",
                description="Work on React projects", required_skills="React,JS,HTML,CSS",
                department="CSE", stipend=15000, duration="6 months", location="Ranchi",
                placement_conversion=True, application_deadline=date(2025, 12, 31), posted_by=u2.id
            )
            session.add(opp)
            session.commit()

# ---------------- AUTH HELPERS ----------------
def verify_user(email, password):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == email)).first()
        if user and pwd_context.verify(password, user.hashed_password):
            return user
    return None

# ---------------- STREAMLIT UI ----------------
def login_ui():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = verify_user(email, password)
        if user:
            st.session_state["user_id"] = user.id
            st.experimental_rerun()
        else:
            st.error("Invalid credentials (try student@example.com / 123)")

# ---------- STUDENT DASHBOARD ----------
def student_dashboard(user: User):
    st.title(f"Welcome, {user.name} 👨‍🎓 (Student)")

    tab1, tab2, tab3, tab4 = st.tabs(["Opportunities", "My Applications", "Preferences", "Recommended"])

    # --- Browse Opportunities ---
    with tab1:
        st.subheader("Browse Opportunities")
        with Session(engine) as session:
            opps = session.exec(select(Opportunity)).all()
            for opp in opps:
                with st.container():
                    st.markdown(f"### {opp.title} at {opp.company}")
                    st.write(opp.description)
                    st.write(f"📍 {opp.location} | 💰 {opp.stipend} | ⏳ {opp.duration}")
                    if st.button(f"Apply to {opp.title}", key=opp.uid):
                        existing = session.exec(
                            select(Application).where(
                                (Application.student_id == user.id) & 
                                (Application.opportunity_id == opp.id)
                            )
                        ).first()
                        if existing:
                            st.warning("Already applied!")
                        else:
                            app = Application(student_id=user.id, opportunity_id=opp.id)
                            session.add(app)
                            session.commit()
                            st.success("Applied successfully!")

    # --- My Applications ---
    with tab2:
        st.subheader("My Applications")
        with Session(engine) as session:
            apps = session.exec(select(Application).where(Application.student_id == user.id)).all()
            for app in apps:
                opp = session.get(Opportunity, app.opportunity_id)
                st.write(f"{opp.title} - Status: {app.status} (Mentor: {app.mentor_status})")

    # --- Preferences ---
    with tab3:
        st.subheader("Preferences")
        with st.form("prefs_form"):
            loc = st.text_input("Preferred Location", value=user.location_pref or "")
            min_stip = st.number_input("Minimum Stipend", value=user.min_stipend_pref or 0)
            max_stip = st.number_input("Maximum Stipend", value=user.max_stipend_pref or 0)
            conv = st.checkbox("Prefer placement conversion", value=user.placement_conversion_pref or False)
            skills_input = st.text_input("Your Skills (comma separated)", value=user.skills or "")
            submitted = st.form_submit_button("Save Preferences")
            if submitted:
                with Session(engine) as session:
                    u = session.get(User, user.id)
                    u.location_pref, u.min_stipend_pref, u.max_stipend_pref, u.placement_conversion_pref, u.skills = loc, min_stip, max_stip, conv, skills_input
                    session.add(u)
                    session.commit()
                    st.success("Preferences saved!")

    # --- Recommendations ---
    with tab4:
        st.subheader("Recommended Opportunities for You")
        with Session(engine) as session:
            opps = session.exec(select(Opportunity)).all()
            matches = []
            student_skills = set((user.skills or "").lower().split(","))

            for opp in opps:
                score = 0
                # Location
                if user.location_pref and user.location_pref.lower() in opp.location.lower():
                    score += 1
                # Stipend
                if user.min_stipend_pref and opp.stipend >= user.min_stipend_pref:
                    score += 1
                if user.max_stipend_pref and opp.stipend <= user.max_stipend_pref:
                    score += 1
                # Placement conversion
                if user.placement_conversion_pref and opp.placement_conversion:
                    score += 1
                # Skill matching
                opp_skills = set(opp.required_skills.lower().split(","))
                skill_matches = len(student_skills & opp_skills)
                score += skill_matches  # 1 point per matching skill

                if score > 0:
                    matches.append((opp, score, skill_matches))

            if not matches:
                st.info("No opportunities match your preferences yet.")
            else:
                matches.sort(key=lambda x: x[1], reverse=True)
                for opp, score, skill_matches in matches:
                    st.markdown(f"### {opp.title} at {opp.company} (Total Score: {score}, Skills Matched: {skill_matches})")
                    st.write(opp.description)
                    st.write(f"📍 {opp.location} | 💰 {opp.stipend} | ⏳ {opp.duration}")

# ---------- FACULTY DASHBOARD ----------
def faculty_dashboard(user: User):
    st.title(f"Welcome, {user.name} 👨‍🏫 (Faculty Mentor)")
    with Session(engine) as session:
        apps = session.exec(select(Application).where(Application.mentor_status == "pending")).all()
        for app in apps:
            student = session.get(User, app.student_id)
            opp = session.get(Opportunity, app.opportunity_id)
            st.markdown(f"**{student.name}** applied for **{opp.title}**")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Approve", key=f"appr-{app.uid}"):
                    app.mentor_status, app.status, app.mentor_comments = "approved", ApplicationStatus.approved, "Approved"
                    session.add(app); session.commit(); st.success("Approved")
            with col2:
                if st.button("Reject", key=f"rej-{app.uid}"):
                    app.mentor_status, app.status, app.mentor_comments = "rejected", ApplicationStatus.rejected, "Rejected"
                    session.add(app); session.commit(); st.error("Rejected")

# ---------- PLACEMENT / EMPLOYER DASHBOARD ----------
def placement_employer_dashboard(user: User):
    st.title(f"Welcome, {user.name} 🏢 ({user.role})")
    tab1, tab2 = st.tabs(["Post Opportunity", "View Applicants"])

    # --- Post Opportunity ---
    with tab1:
        with st.form("post_opp_form"):
            title = st.text_input("Title")
            company = st.text_input("Company")
            desc = st.text_area("Description")
            skills = st.text_input("Required Skills (comma separated)")
            dept = st.text_input("Department")
            stipend = st.number_input("Stipend", 0)
            dur = st.text_input("Duration")
            loc = st.text_input("Location")
            conv = st.checkbox("Placement Conversion")
            deadline = st.date_input("Deadline")
            submitted = st.form_submit_button("Post Opportunity")

            if submitted:
                if not (title and company and desc and skills and dept and loc):
                    st.warning("Please fill all mandatory fields!")
                else:
                    with Session(engine) as session:
                        opp = Opportunity(
                            title=title, company=company, description=desc,
                            required_skills=skills, department=dept, stipend=stipend,
                            duration=dur, location=loc, placement_conversion=conv,
                            application_deadline=deadline, posted_by=user.id
                        )
                        session.add(opp); session.commit()
                        st.success("Posted successfully!")

    # --- View Applicants ---
    with tab2:
        with Session(engine) as session:
            opps = session.exec(select(Opportunity).where(Opportunity.posted_by == user.id)).all()
            for opp in opps:
                st.markdown(f"### {opp.title}")
                apps = session.exec(select(Application).where(Application.opportunity_id == opp.id)).all()
                for app in apps:
                    stu = session.get(User, app.student_id)
                    st.write(f"- {stu.name} ({stu.email}) - Status: {app.status}")

# ---------------- MAIN APP ----------------
def main():
    st.set_page_config(page_title="CampusConnect", page_icon="🎓", layout="wide")
    create_db_and_seed()

    user_id = st.session_state.get("user_id")
    user = None
    if user_id:
        with Session(engine) as session:
            user = session.get(User, user_id)

    if not user:
        login_ui()
    else:
        st.sidebar.write(f"Logged in as: {user.name} ({user.role})")
        if st.sidebar.button("Logout"):
            st.session_state.pop("user_id")
            st.experimental_rerun()

        if user.role == Role.student:
            student_dashboard(user)
        elif user.role == Role.facultyMentor:
            faculty_dashboard(user)
        else:
            placement_employer_dashboard(user)

if __name__ == "__main__":
    main()


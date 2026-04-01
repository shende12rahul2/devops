import streamlit as st
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, date
import random

# ─── Configuration ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DevOps Command Center",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = Path(__file__).parent / "progress.json"

# ─── Session State Management ─────────────────────────────────────────────────
def init_session_state():
    """Initialize comprehensive session state for 48 weeks and 12 projects."""
    # Core progress tracking
    st.session_state.setdefault("current_week", 1)
    st.session_state.setdefault("current_project", 1)
    st.session_state.setdefault("current_question", 1)

    # Completion percentages (0-100)
    st.session_state.setdefault("week_completion", {f"week_{i}": 0.0 for i in range(1, 49)})
    st.session_state.setdefault("project_completion", {f"project_{i}": 0.0 for i in range(1, 13)})

    # Detailed tracking
    st.session_state.setdefault("week_details", {
        f"week_{i}": {
            "labs_completed": 0,
            "labs_total": 5,
            "interview_prep_completed": 0,
            "interview_prep_total": 15,
            "project_completed": False,
            "hours_logged": 0.0,
            "hours_target": 40.0,
            "notes": "",
            "rating": 0
        } for i in range(1, 49)
    })

    st.session_state.setdefault("project_details", {
        f"project_{i}": {
            "name": f"Project {i}",
            "description": f"Enterprise project {i} implementation",
            "status": "not_started",  # not_started, in_progress, completed
            "github_url": "",
            "business_impact": "",
            "completion_percentage": 0.0,
            "start_date": None,
            "end_date": None
        } for i in range(1, 13)
    })

    # Executive metrics
    st.session_state.setdefault("executive_metrics", {
        "total_weeks_completed": 0,
        "total_projects_completed": 0,
        "overall_completion_pct": 0.0,
        "avg_week_rating": 0.0,
        "total_hours_logged": 0.0,
        "certifications_earned": 0,
        "interview_questions_practiced": 0
    })

    # User profile
    st.session_state.setdefault("profile", {
        "name": "DevOps Engineer",
        "start_date": str(date.today()),
        "target_role": "Senior/Staff DevOps Engineer",
        "current_streak": 0,
        "total_hours_logged": 0.0,
        "github_url": "",
        "linkedin_url": ""
    })

def calculate_completion_percentages():
    """Calculate completion percentages for weeks and projects."""
    # Week completion
    for week_num in range(1, 49):
        week_key = f"week_{week_num}"
        week_data = st.session_state.week_details[week_key]

        labs_pct = (week_data["labs_completed"] / week_data["labs_total"]) * 0.4
        interview_pct = (week_data["interview_prep_completed"] / week_data["interview_prep_total"]) * 0.4
        project_pct = (1.0 if week_data["project_completed"] else 0.0) * 0.2

        total_pct = labs_pct + interview_pct + project_pct
        st.session_state.week_completion[week_key] = min(total_pct, 1.0)

    # Project completion
    for proj_num in range(1, 13):
        proj_key = f"project_{proj_num}"
        proj_data = st.session_state.project_details[proj_key]

        if proj_data["status"] == "completed":
            st.session_state.project_completion[proj_key] = 1.0
        elif proj_data["status"] == "in_progress":
            st.session_state.project_completion[proj_key] = 0.5
        else:
            st.session_state.project_completion[proj_key] = 0.0

def save_progress():
    """Save all progress data to JSON file."""
    data = {
        "current_week": st.session_state.current_week,
        "current_project": st.session_state.current_project,
        "current_question": st.session_state.current_question,
        "week_completion": st.session_state.week_completion,
        "project_completion": st.session_state.project_completion,
        "week_details": st.session_state.week_details,
        "project_details": st.session_state.project_details,
        "executive_metrics": st.session_state.executive_metrics,
        "profile": st.session_state.profile,
        "last_saved": str(datetime.now())
    }

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

def load_progress():
    """Load progress data from JSON file."""
    if not DATA_FILE.exists():
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Load all the data back into session state
        st.session_state.current_week = data.get("current_week", 1)
        st.session_state.current_project = data.get("current_project", 1)
        st.session_state.current_question = data.get("current_question", 1)
        st.session_state.week_completion = data.get("week_completion", st.session_state.week_completion)
        st.session_state.project_completion = data.get("project_completion", st.session_state.project_completion)
        st.session_state.week_details = data.get("week_details", st.session_state.week_details)
        st.session_state.project_details = data.get("project_details", st.session_state.project_details)
        st.session_state.executive_metrics = data.get("executive_metrics", st.session_state.executive_metrics)
        st.session_state.profile = data.get("profile", st.session_state.profile)

    except Exception as e:
        st.error(f"Error loading progress: {e}")

# ─── Page Functions ───────────────────────────────────────────────────────────

def dashboard():
    """Main dashboard with executive overview."""
    st.title("🚀 DevOps Command Center")

    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        weeks_completed = sum(1 for pct in st.session_state.week_completion.values() if pct >= 1.0)
        st.metric("Weeks Completed", f"{weeks_completed}/48", f"{(weeks_completed/48*100):.1f}%")

    with col2:
        projects_completed = sum(1 for pct in st.session_state.project_completion.values() if pct >= 1.0)
        st.metric("Projects Completed", f"{projects_completed}/12", f"{(projects_completed/12*100):.1f}%")

    with col3:
        total_hours = sum(week["hours_logged"] for week in st.session_state.week_details.values())
        st.metric("Hours Logged", f"{total_hours:.1f}h")

    with col4:
        avg_rating = sum(week["rating"] for week in st.session_state.week_details.values() if week["rating"] > 0) / max(1, sum(1 for week in st.session_state.week_details.values() if week["rating"] > 0))
        st.metric("Avg Week Rating", f"{avg_rating:.1f}/5")

    # Progress visualizations
    st.subheader("📊 Progress Overview")

    # Week completion heatmap
    week_data = []
    for week_num in range(1, 49):
        week_key = f"week_{week_num}"
        completion = st.session_state.week_completion[week_key]
        week_data.append({
            "Week": week_num,
            "Completion": completion * 100,
            "Status": "Complete" if completion >= 1.0 else "In Progress" if completion > 0 else "Not Started"
        })

    week_df = pd.DataFrame(week_data)
    st.bar_chart(week_df.set_index("Week")["Completion"])

    # Current week focus
    st.subheader(f"🎯 Current Week {st.session_state.current_week} Focus")
    current_week_data = st.session_state.week_details[f"week_{st.session_state.current_week}"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Labs", f"{current_week_data['labs_completed']}/{current_week_data['labs_total']}")
    with col2:
        st.metric("Interview Prep", f"{current_week_data['interview_prep_completed']}/{current_week_data['interview_prep_total']}")
    with col3:
        st.metric("Hours", f"{current_week_data['hours_logged']:.1f}/{current_week_data['hours_target']}h")

def week_tracker():
    """Detailed week-by-week tracking."""
    st.title("📅 Week Tracker")

    # Week selector
    selected_week = st.selectbox("Select Week", range(1, 49), index=st.session_state.current_week-1)

    week_key = f"week_{selected_week}"
    week_data = st.session_state.week_details[week_key]

    st.subheader(f"Week {selected_week} Progress")

    # Progress inputs
    col1, col2, col3 = st.columns(3)

    with col1:
        labs_completed = st.number_input("Labs Completed", 0, week_data["labs_total"],
                                       week_data["labs_completed"], key=f"labs_{selected_week}")
        if labs_completed != week_data["labs_completed"]:
            st.session_state.week_details[week_key]["labs_completed"] = labs_completed

    with col2:
        interview_completed = st.number_input("Interview Questions", 0, week_data["interview_prep_total"],
                                            week_data["interview_prep_completed"], key=f"interview_{selected_week}")
        if interview_completed != week_data["interview_prep_completed"]:
            st.session_state.week_details[week_key]["interview_prep_completed"] = interview_completed

    with col3:
        hours_logged = st.number_input("Hours Logged", 0.0, 80.0,
                                     week_data["hours_logged"], 0.5, key=f"hours_{selected_week}")
        if hours_logged != week_data["hours_logged"]:
            st.session_state.week_details[week_key]["hours_logged"] = hours_logged

    # Project completion
    project_done = st.checkbox("Project Completed", week_data["project_completed"], key=f"project_{selected_week}")
    if project_done != week_data["project_completed"]:
        st.session_state.week_details[week_key]["project_completed"] = project_done

    # Notes and rating
    notes = st.text_area("Week Notes", week_data["notes"], key=f"notes_{selected_week}")
    if notes != week_data["notes"]:
        st.session_state.week_details[week_key]["notes"] = notes

    rating = st.slider("Week Rating (1-5)", 1, 5, max(week_data["rating"], 1), key=f"rating_{selected_week}")
    if rating != week_data["rating"]:
        st.session_state.week_details[week_key]["rating"] = rating

    # Recalculate completion
    calculate_completion_percentages()

def project_portfolio():
    """Project portfolio management."""
    st.title("🏗️ Project Portfolio")

    # Project selector
    selected_project = st.selectbox("Select Project", range(1, 13), index=st.session_state.current_project-1)

    project_key = f"project_{selected_project}"
    project_data = st.session_state.project_details[project_key]

    st.subheader(f"Project {selected_project}: {project_data['name']}")

    # Project details
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Project Name", project_data["name"], key=f"name_{selected_project}")
        if name != project_data["name"]:
            st.session_state.project_details[project_key]["name"] = name

        status_options = ["not_started", "in_progress", "completed"]
        status = st.selectbox("Status", status_options,
                            index=status_options.index(project_data["status"]),
                            key=f"status_{selected_project}")
        if status != project_data["status"]:
            st.session_state.project_details[project_key]["status"] = status

    with col2:
        github_url = st.text_input("GitHub URL", project_data["github_url"], key=f"github_{selected_project}")
        if github_url != project_data["github_url"]:
            st.session_state.project_details[project_key]["github_url"] = github_url

    # Business impact
    business_impact = st.text_area("Business Impact", project_data["business_impact"],
                                 height=100, key=f"impact_{selected_project}")
    if business_impact != project_data["business_impact"]:
        st.session_state.project_details[project_key]["business_impact"] = business_impact

    # Recalculate completion
    calculate_completion_percentages()

def roadmap_view():
    """48-week roadmap visualization."""
    st.title("🗓️ 48-Week Roadmap")

    # Roadmap phases
    phases = {
        "Phase 1 (Weeks 1-4)": {"weeks": range(1, 5), "color": "#4F46E5", "focus": "Foundations"},
        "Phase 2 (Weeks 5-10)": {"weeks": range(5, 11), "color": "#0891B2", "focus": "Core DevOps"},
        "Phase 3 (Weeks 11-18)": {"weeks": range(11, 19), "color": "#D97706", "focus": "Enterprise"},
        "Phase 4 (Weeks 19-26)": {"weeks": range(19, 27), "color": "#16A34A", "focus": "Architecture"},
        "Phase 5 (Weeks 27-36)": {"weeks": range(27, 37), "color": "#DC2626", "focus": "Leadership"},
        "Phase 6 (Weeks 37-48)": {"weeks": range(37, 49), "color": "#7C3AED", "focus": "Expertise"}
    }

    for phase_name, phase_data in phases.items():
        with st.expander(f"📚 {phase_name} - {phase_data['focus']}", expanded=False):
            cols = st.columns(len(phase_data["weeks"]))

            for i, week_num in enumerate(phase_data["weeks"]):
                with cols[i]:
                    week_key = f"week_{week_num}"
                    completion = st.session_state.week_completion[week_key]

                    if completion >= 1.0:
                        st.success(f"Week {week_num}")
                    elif completion > 0:
                        st.warning(f"Week {week_num}")
                    else:
                        st.info(f"Week {week_num}")

                    st.progress(completion)
                    st.caption(f"{completion*100:.0f}%")

def interview_prep():
    """Interview preparation tracking."""
    st.title("🎤 Interview Preparation")

    st.metric("Questions Practiced", st.session_state.current_question - 1)
    st.metric("Completion Rate", f"{((st.session_state.current_question - 1) / 300 * 100):.1f}%")

    # Progress bar
    st.progress((st.session_state.current_question - 1) / 300)

    # Question advancement
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Previous Question"):
            st.session_state.current_question = max(1, st.session_state.current_question - 1)
            st.rerun()

    with col2:
        st.write(f"**Question {st.session_state.current_question}/300**")

    with col3:
        if st.button("Next Question ➡️"):
            st.session_state.current_question = min(300, st.session_state.current_question + 1)
            st.rerun()

def certifications():
    """Certification tracking."""
    st.title("🎓 Certifications")

    certifications = [
        {"name": "CKA", "full_name": "Certified Kubernetes Administrator", "status": "not_started"},
        {"name": "CKAD", "full_name": "Certified Kubernetes Application Developer", "status": "not_started"},
        {"name": "CKS", "full_name": "Certified Kubernetes Security Specialist", "status": "not_started"},
        {"name": "AWS SAP", "full_name": "AWS Solutions Architect Professional", "status": "not_started"},
        {"name": "Terraform Associate", "full_name": "HashiCorp Terraform Associate", "status": "not_started"}
    ]

    for cert in certifications:
        with st.expander(f"📜 {cert['name']} - {cert['full_name']}", expanded=False):
            status = st.selectbox(f"Status for {cert['name']}",
                                ["not_started", "studying", "scheduled", "passed"],
                                key=f"cert_{cert['name']}")
            target_date = st.date_input(f"Target Date for {cert['name']}",
                                      key=f"date_{cert['name']}")
            notes = st.text_area(f"Study Notes for {cert['name']}",
                               key=f"notes_{cert['name']}", height=80)

def daily_log():
    """Daily learning log."""
    st.title("📓 Daily Log")

    # Quick log entry
    with st.form("daily_entry"):
        col1, col2 = st.columns(2)

        with col1:
            log_date = st.date_input("Date", date.today())
            hours = st.number_input("Hours", 0.0, 12.0, 2.0, 0.5)

        with col2:
            activity_type = st.selectbox("Activity Type",
                                       ["Morning Study", "Evening Lab", "Project Work", "Interview Prep", "Review"])
            week_num = st.number_input("Week #", 1, 48, st.session_state.current_week)

        topic = st.text_input("Topic Covered")
        achievements = st.text_area("What I Built/Accomplished", height=80)
        challenges = st.text_area("Challenges Faced", height=60)
        insights = st.text_input("Key Insight")

        submitted = st.form_submit_button("Log Session")
        if submitted:
            st.success("Session logged successfully!")

def analytics():
    """Progress analytics and insights."""
    st.title("📊 Analytics & Insights")

    # Completion trends
    st.subheader("📈 Completion Trends")

    # Calculate metrics
    total_weeks = sum(1 for pct in st.session_state.week_completion.values() if pct > 0)
    completed_weeks = sum(1 for pct in st.session_state.week_completion.values() if pct >= 1.0)
    total_projects = sum(1 for pct in st.session_state.project_completion.values() if pct > 0)
    completed_projects = sum(1 for pct in st.session_state.project_completion.values() if pct >= 1.0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Weeks", total_weeks)
    with col2:
        st.metric("Completed Weeks", completed_weeks)
    with col3:
        st.metric("Active Projects", total_projects)
    with col4:
        st.metric("Completed Projects", completed_projects)

    # Weekly progress chart
    week_progress_data = []
    for week in range(1, 49):
        week_progress_data.append({
            "Week": week,
            "Completion %": st.session_state.week_completion[f"week_{week}"] * 100
        })

    progress_df = pd.DataFrame(week_progress_data)
    st.line_chart(progress_df.set_index("Week"))

def settings():
    """User settings and profile."""
    st.title("⚙️ Settings & Profile")

    st.subheader("👤 Profile Information")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name", st.session_state.profile["name"])
        if name != st.session_state.profile["name"]:
            st.session_state.profile["name"] = name

        target_role = st.text_input("Target Role", st.session_state.profile["target_role"])
        if target_role != st.session_state.profile["target_role"]:
            st.session_state.profile["target_role"] = target_role

    with col2:
        github_url = st.text_input("GitHub URL", st.session_state.profile["github_url"])
        if github_url != st.session_state.profile["github_url"]:
            st.session_state.profile["github_url"] = github_url

        linkedin_url = st.text_input("LinkedIn URL", st.session_state.profile.get("linkedin_url", ""))
        if linkedin_url != st.session_state.profile.get("linkedin_url", ""):
            st.session_state.profile["linkedin_url"] = linkedin_url

    st.subheader("💾 Data Management")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Save Progress"):
            save_progress()
            st.success("Progress saved!")

    with col2:
        if st.button("📂 Load Progress"):
            load_progress()
            st.success("Progress loaded!")

    with col3:
        if st.button("🔄 Recalculate Metrics"):
            calculate_completion_percentages()
            st.success("Metrics recalculated!")

def achievements():
    """Achievements and milestones."""
    st.title("🏆 Achievements & Milestones")

    # Calculate achievements
    completed_weeks = sum(1 for pct in st.session_state.week_completion.values() if pct >= 1.0)
    completed_projects = sum(1 for pct in st.session_state.project_completion.values() if pct >= 1.0)
    total_hours = sum(week["hours_logged"] for week in st.session_state.week_details.values())

    achievements = []

    if completed_weeks >= 1:
        achievements.append({"icon": "🎯", "title": "First Week Complete", "desc": "Completed your first week of training"})
    if completed_weeks >= 4:
        achievements.append({"icon": "🏔️", "title": "Phase 1 Complete", "desc": "Mastered DevOps foundations"})
    if completed_weeks >= 10:
        achievements.append({"icon": "⚡", "title": "Core DevOps Stack", "desc": "Built complete DevOps toolkit"})
    if completed_projects >= 1:
        achievements.append({"icon": "🏗️", "title": "First Project", "desc": "Completed your first enterprise project"})
    if total_hours >= 100:
        achievements.append({"icon": "⏰", "title": "Century Club", "desc": "Logged 100+ hours of study"})
    if total_hours >= 500:
        achievements.append({"icon": "🔥", "title": "Dedication", "desc": "500+ hours invested in growth"})

    for achievement in achievements:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(achievement["icon"])
        with col2:
            st.subheader(achievement["title"])
            st.write(achievement["desc"])
        st.divider()

def resources():
    """Learning resources and references."""
    st.title("📚 Resources & References")

    st.subheader("🔗 Key Learning Resources")

    resources = [
        {"name": "Kubernetes Documentation", "url": "https://kubernetes.io/docs/", "desc": "Official K8s docs"},
        {"name": "AWS Documentation", "url": "https://docs.aws.amazon.com/", "desc": "AWS services reference"},
        {"name": "Terraform Registry", "url": "https://registry.terraform.io/", "desc": "Terraform modules"},
        {"name": "Docker Docs", "url": "https://docs.docker.com/", "desc": "Container platform docs"},
        {"name": "GitHub Actions", "url": "https://docs.github.com/en/actions", "desc": "CI/CD workflows"}
    ]

    for resource in resources:
        with st.expander(f"📖 {resource['name']}", expanded=False):
            st.write(resource["desc"])
            st.markdown(f"[Visit Resource]({resource['url']})")

def community():
    """Community and networking."""
    st.title("🤝 Community & Networking")

    st.subheader("🌐 DevOps Communities")

    communities = [
        {"name": "DevOps subreddit", "url": "https://reddit.com/r/devops", "desc": "Active DevOps discussion"},
        {"name": "Kubernetes Slack", "url": "https://slack.k8s.io/", "desc": "K8s community chat"},
        {"name": "CNCF Community", "url": "https://www.cncf.io/community/", "desc": "Cloud Native Computing"},
        {"name": "AWS User Groups", "url": "https://aws.amazon.com/usergroups/", "desc": "Local AWS meetups"}
    ]

    for community in communities:
        with st.expander(f"👥 {community['name']}", expanded=False):
            st.write(community["desc"])
            st.markdown(f"[Join Community]({community['url']})")

# ─── Navigation ───────────────────────────────────────────────────────────────

PAGE_FUNCTIONS = {
    "🏠 Dashboard": dashboard,
    "📅 Week Tracker": week_tracker,
    "🏗️ Project Portfolio": project_portfolio,
    "🗓️ Roadmap View": roadmap_view,
    "🎤 Interview Prep": interview_prep,
    "🎓 Certifications": certifications,
    "📓 Daily Log": daily_log,
    "📊 Analytics": analytics,
    "🏆 Achievements": achievements,
    "📚 Resources": resources,
    "🤝 Community": community,
    "⚙️ Settings": settings
}

def render_sidebar():
    """Render the comprehensive sidebar navigation."""
    st.sidebar.title("🚀 Command Center")

    # Profile summary
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**👋 {st.session_state.profile['name']}**")
    st.sidebar.markdown(f"*{st.session_state.profile['target_role']}*")

    # Progress summary
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Progress Summary**")

    weeks_completed = sum(1 for pct in st.session_state.week_completion.values() if pct >= 1.0)
    projects_completed = sum(1 for pct in st.session_state.project_completion.values() if pct >= 1.0)

    st.sidebar.progress(weeks_completed / 48)
    st.sidebar.caption(f"Weeks: {weeks_completed}/48")

    st.sidebar.progress(projects_completed / 12)
    st.sidebar.caption(f"Projects: {projects_completed}/12")

    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🧭 Navigation**")

    page = st.sidebar.radio(
        "Select Section",
        list(PAGE_FUNCTIONS.keys()),
        index=0,
        label_visibility="collapsed"
    )

    # Quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown("**⚡ Quick Actions**")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.sidebar.button("💾 Save"):
            save_progress()
            st.sidebar.success("Saved!")

    with col2:
        if st.sidebar.button("📂 Load"):
            load_progress()
            st.sidebar.success("Loaded!")

    # Current focus
    st.sidebar.markdown("---")
    st.sidebar.markdown("**🎯 Current Focus**")
    st.sidebar.write(f"Week: {st.session_state.current_week}/48")
    st.sidebar.write(f"Project: {st.session_state.current_project}/12")
    st.sidebar.write(f"Question: {st.session_state.current_question}/300")

    return page

# ─── Main Application ─────────────────────────────────────────────────────────

def main():
    """Main application entry point."""
    init_session_state()
    load_progress()
    calculate_completion_percentages()

    selected_page = render_sidebar()
    PAGE_FUNCTIONS[selected_page]()

if __name__ == "__main__":
    main()

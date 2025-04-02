import streamlit as st

st.title("AI-Powered CV Generator")

with st.form("cv_form"):
    st.header("Personal Details")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn Profile URL")

    st.header("Professional Experience")
    experience = st.text_area("Describe your work experience")

    st.header("Education History")
    education = st.text_area("List your education history")

    st.header("Skills & Certifications")
    skills = st.text_area("List your skills and certifications")

    st.header("Job Position or Career Goal")
    job_position = st.text_input("Target Job Position")

    submitted = st.form_submit_button("Generate CV")

    if submitted:
        if not all([name, email, phone, linkedin, experience, education,
                    skills, job_position]):
            st.error("⚠️ Please fill in all the fields before submitting!")
        else:
            st.success("✅ Check your information! Processing...")
            st.write("### Summary of Your Input:")
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Phone:** {phone}")
            st.write(f"**LinkedIn:** {linkedin}")
            st.write(f"**Experience:** {experience}")
            st.write(f"**Education:** {education}")
            st.write(f"**Skills:** {skills}")
            st.write(f"**Target Job Position:** {job_position}")

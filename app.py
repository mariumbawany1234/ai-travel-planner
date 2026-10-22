"""
AI Travel Planner
Streamlit UI powered by Groq LLM
Run:
streamlit run app.py
"""

import streamlit as st
from pathlib import Path

from groq_client import generate, DEFAULT_MODEL
from prompts import Traveler, TECHNIQUES


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)



# ==============================
# LOAD CSS
# ==============================

def load_css():

    css_file = Path("assets/style.css")

    if css_file.exists():

        with open(css_file, "r", encoding="utf-8") as file:

            st.markdown(
                f"""
                <style>
                {file.read()}
                </style>
                """,
                unsafe_allow_html=True
            )


load_css()



# ==============================
# SIDEBAR
# ==============================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-title">
            ⚙️ Settings
        </div>
        """,
        unsafe_allow_html=True
    )


    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Enter API key"
    )


    model = st.text_input(
        "AI Model",
        value=DEFAULT_MODEL
    )


    temperature = st.slider(
        "Creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )


    st.divider()


    st.markdown(
        """
        <div class="side-info">

        <h4>AI Capabilities</h4>

        ✓ Zero-shot prompting<br>
        ✓ Few-shot prompting<br>
        ✓ Role-based prompting<br>
        ✓ Groq LLM integration<br>
        ✓ Personalized planning

        </div>
        """,
        unsafe_allow_html=True
    )



# ==============================
# HERO SECTION
# ==============================

st.markdown(
    """
    <div class="hero">


        <div class="hero-icon">
            ✈️
        </div>


        <h1>
            AI Travel Planner
        </h1>


        <p>
            Generate personalized travel itineraries
            using Groq LLMs and advanced prompt engineering.
        </p>


    </div>
    """,
    unsafe_allow_html=True
)



# ==============================
# FEATURE CARDS
# ==============================


features = [

    ("🧠", "Prompt Engineering"),

    ("⚡", "Groq LLM"),

    ("🌍", "Smart Planning"),

    ("🚀", "AI Generation")

]


columns = st.columns(4)


for column, item in zip(columns, features):

    with column:

        st.markdown(
            f"""
            <div class="feature-card">

                <div class="feature-icon">

                    {item[0]}

                </div>


                <div class="feature-title">

                    {item[1]}

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )



st.write("")



# ==============================
# SECTION TITLE
# ==============================


st.markdown(
    """
    <div class="section-title">

        🧳 Create Your Trip

    </div>
    """,
    unsafe_allow_html=True
)

# ==============================
# TRAVEL FORM
# ==============================


with st.form("travel_form"):


    col1, col2 = st.columns(2)


    with col1:

        name = st.text_input(
            "Traveler Name",
            value="Alex"
        )


        destination = st.text_input(
            "Destination",
            value="Dubai"
        )


    with col2:

        days = st.number_input(
            "Number of Days",
            min_value=1,
            max_value=30,
            value=5
        )


        budget = st.number_input(
            "Budget (USD)",
            min_value=50,
            max_value=100000,
            value=1000,
            step=50
        )



    style = st.selectbox(

        "Travel Style",

        [
            "Solo",
            "Family",
            "Friends",
            "Luxury",
            "Adventure"
        ]

    )



    interests = st.multiselect(

        "Travel Interests",

        [
            "Food",
            "Nature",
            "Adventure",
            "Shopping",
            "History",
            "Culture",
            "Beaches",
            "Nightlife",
            "Relaxation",
            "Art"
        ],

        default=[
            "Food",
            "Culture"
        ]

    )



    technique = st.radio(

        "Prompt Strategy",

        list(TECHNIQUES.keys()) + ["Compare All Three"],

        horizontal=True

    )



    submitted = st.form_submit_button(

        "✨ Generate AI Itinerary"

    )



# ==============================
# GENERATION FUNCTION
# ==============================


def generate_itinerary(
        technique_name,
        traveler
):


    prompt = TECHNIQUES[technique_name](traveler)


    with st.spinner(
        f"Generating using {technique_name}..."
    ):


        response, seconds = generate(

            prompt,

            api_key=api_key or None,

            model=model,

            temperature=temperature

        )


    return response, seconds, prompt




# ==============================
# DISPLAY RESULT
# ==============================


if submitted:


    if not interests:

        st.warning(
            "Please select at least one interest."
        )

        st.stop()



    traveler = Traveler(

        name,

        destination,

        int(days),

        float(budget),

        interests,

        style

    )



    st.markdown(
        """
        <div class="section-title">

        🤖 AI Generated Itinerary

        </div>
        """,
        unsafe_allow_html=True
    )



    try:


        # Compare all prompting techniques

        if technique == "Compare All Three":


            result_columns = st.columns(3)



            for column, method in zip(
                result_columns,
                TECHNIQUES
            ):


                with column:


                    st.subheader(method)



                    output, seconds, prompt = generate_itinerary(

                        method,

                        traveler

                    )


                    with st.container(border=True):

                        st.markdown(output)


                    st.caption(

                        f"Generated in {seconds:.2f}s"

                    )


                    with st.expander(
                        "View Prompt"
                    ):

                        st.code(

                            prompt,

                            language="text"

                        )



        else:


            output, seconds, prompt = generate_itinerary(

                technique,

                traveler

            )


            with st.container(border=True):

                st.markdown(output)



            st.success(

                f"Completed in {seconds:.2f} seconds"

            )



            col1, col2 = st.columns([1,1])


            with col1:

                st.download_button(

                    label="📥 Download Itinerary",

                    data=output,

                    file_name=f"{destination}_travel_plan.md",

                    mime="text/markdown"

                )


            with col2:

                st.metric(

                    "AI Model",

                    model

                )



            with st.expander(
                "🔍 View Generated Prompt"
            ):

                st.code(

                    prompt,

                    language="text"

                )



    except Exception as error:


        st.error(

            f"Something went wrong: {error}"

        )



# ==============================
# FOOTER
# ==============================


st.markdown(
    """
    <br>

    <div class="footer">

    Built with ❤️ using Python, Streamlit, Groq LLMs
    and Prompt Engineering

    </div>

    """,
    unsafe_allow_html=True
)
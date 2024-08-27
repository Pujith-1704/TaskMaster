import streamlit as st
import pandas as pd

# Initialize a DataFrame in session state (this could be loaded from a file for persistent storage)
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Task", "Description"])

# Function to reset the edit state and input fields
def reset_edit_state():
    st.session_state.task = ""
    st.session_state.description = ""
    if 'editing_idx' in st.session_state:
        del st.session_state.editing_idx
        del st.session_state.task_edit
        del st.session_state.desc_edit

# Initialize task and description fields
if 'task' not in st.session_state:
    st.session_state.task = ""

if 'description' not in st.session_state:
    st.session_state.description = ""
    
# Display a centered, large title
st.markdown(
    """
    <h1 style="text-align: center; color: #333;"><u>TaskMaster</u></h1>
    <h3 style="text-align: center; color: #333;">Your Interactive Task Organizer</h3>
    """,
    unsafe_allow_html=True
)

# Apply custom CSS to add padding to the button's container
st.markdown(
    """
    <style>
    .button-container {
        margin-top: 26px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a form for data entry and search
with st.form("task_form", clear_on_submit=True):
    task_col, button_col = st.columns([4, 1])
    with task_col:
        task = st.text_input("Task", value=st.session_state.task, key="task_input")
    with button_col:
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        search_submitted = st.form_submit_button("Search")
        st.markdown('</div>', unsafe_allow_html=True)

        description = st.text_input("Description", value=st.session_state.description, key="desc_input")
    submitted = st.form_submit_button("Create")

    if submitted and task:
        # Create a new DataFrame row and concatenate with the existing DataFrame
        new_entry = pd.DataFrame({"Task": [task], "Description": [description]})
        st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
        st.success("Task added successfully!")

        # Clear the input fields after submission
        reset_edit_state()

    # Handle search functionality
    if search_submitted and task:
        st.session_state.highlight_task = task
    else:
        st.session_state.highlight_task = None

# Display the DataFrame in the app
st.write("## Current Tasks")
for idx, row in st.session_state.data.iterrows():
    is_highlighted = row['Task'] == st.session_state.highlight_task
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        task_style = (
            "background-color: #ffcccc; border: 2px solid red; padding: 10px; border-radius: 5px;"
            if is_highlighted
            else "padding: 10px; border-radius: 5px;"
        )
        st.markdown(
            f"""
            <div style="{task_style}">
                <b>{row['Task']}:</b> {row['Description']}
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        edit_button = st.button("Edit", key=f"edit_{idx}")
        if edit_button:
            st.session_state.editing_idx = idx
            st.session_state.task_edit = row['Task']
            st.session_state.desc_edit = row['Description']
    with col3:
        delete_button = st.button("Delete", key=f"delete_{idx}")
        if delete_button:
            st.session_state.data = st.session_state.data.drop(idx).reset_index(drop=True)
            st.success("Task deleted successfully!")
            reset_edit_state()

# Handle editing
if 'editing_idx' in st.session_state:
    st.write("## Edit Task")
    with st.form("edit_form"):
        new_task = st.text_input("Task", value=st.session_state.task_edit)
        new_description = st.text_input("Description", value=st.session_state.desc_edit)
        update_submitted = st.form_submit_button("Update")

        if update_submitted:
            st.session_state.data.at[st.session_state.editing_idx, "Task"] = new_task
            st.session_state.data.at[st.session_state.editing_idx, "Description"] = new_description
            st.success("Task updated successfully!")
            reset_edit_state()
    

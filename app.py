# -*- coding: utf-8 -*-
import streamlit as st
import os
from datetime import datetime
from pathlib import Path
import sys
import io
import logging
import threading
import time
import re
from contextlib import redirect_stdout, redirect_stderr
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dev_aem_crew_sys.crew import DevAemCrewSys

# Set up logging to capture crew logs
log_file = "crew_execution.log"

# Create a custom handler that writes to file and can be monitored
class StreamlitLogHandler(logging.Handler):
    def __init__(self, log_list):
        super().__init__()
        self.log_list = log_list

    def emit(self, record):
        log_entry = self.format(record)
        self.log_list.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": record.levelname.lower(),
            "message": log_entry
        })

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Page configuration
st.set_page_config(
    page_title="AEMplify - Design to AEM Component Converter",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #4B3C99;
        --secondary-color: #E85C23;
        --success-color: #28a745;
        --error-color: #dc3545;
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #4B3C99 0%, #E85C23 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }

    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }

    /* Log container */
    .log-container {
        background: #1e1e1e;
        color: #00ff00;
        padding: 1.5rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        max-height: 600px;
        overflow-y: auto;
        margin-top: 1rem;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }

    .log-entry {
        margin: 0.3rem 0;
        line-height: 1.5;
    }

    .log-info { color: #00d4ff; }
    .log-success { color: #00ff00; }
    .log-warning { color: #ffa500; }
    .log-error { color: #ff4444; }

    /* Agent badges */
    .agent-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.5rem;
        font-weight: 600;
        color: white;
    }

    .agent-designer { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .agent-developer { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .agent-aem { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }

    /* Status indicators */
    .status-ready { color: #28a745; }
    .status-running { color: #ffa500; animation: pulse 2s infinite; }
    .status-complete { color: #4B3C99; }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #4B3C99 0%, #E85C23 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
        transition: transform 0.2s;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(75, 60, 153, 0.4);
    }

    /* Upload box */
    .uploadedFile {
        border: 2px dashed #4B3C99;
        border-radius: 10px;
        padding: 1rem;
    }

    /* Simplified Professional Timeline */
    .timeline-section {
        margin: 1.5rem 0;
        padding: 1rem 1.5rem;
        background: #ffffff;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }

    .timeline-horizontal {
        display: flex;
        justify-content: space-around;
        align-items: flex-start;
        position: relative;
        padding: 1rem 0.5rem;
        gap: 1.5rem;
    }

    /* Simple connecting line */
    .timeline-horizontal::before {
        content: '';
        position: absolute;
        top: 30px;
        left: 20%;
        right: 20%;
        height: 2px;
        background: #dee2e6;
        z-index: 0;
    }

    .agent-column {
        flex: 1;
        text-align: center;
        position: relative;
        z-index: 1;
        max-width: 180px;
    }

    /* Clean icon container */
    .agent-icon-container {
        width: 60px;
        height: 60px;
        margin: 0 auto 0.75rem;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        position: relative;
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        transition: all 0.3s ease;
    }

    .agent-icon-container.pending {
        background: #f8f9fa;
        border-color: #dee2e6;
        opacity: 0.6;
    }

    .agent-icon-container.active {
        background: #fff3cd;
        border-color: #ffc107;
        transform: scale(1.05);
        box-shadow: 0 3px 10px rgba(255, 193, 7, 0.3);
    }

    .agent-icon-container.completed {
        background: #d4edda;
        border-color: #28a745;
    }

    /* Simple status badge */
    .agent-status-badge {
        position: absolute;
        top: -5px;
        right: -5px;
        width: 22px;
        height: 22px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.75rem;
        font-weight: bold;
        background: white;
        border: 2px solid white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }

    .agent-status-badge.pending {
        background: #6c757d;
        color: white;
    }

    .agent-status-badge.active {
        background: #ffc107;
        color: white;
        animation: pulse-badge 1.5s infinite;
    }

    .agent-status-badge.completed {
        background: #28a745;
        color: white;
    }

    @keyframes pulse-badge {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.15); }
    }

    /* Agent name */
    .agent-name-display {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.4rem;
        color: #2c3e50;
    }

    .agent-name-display.pending { color: #6c757d; }
    .agent-name-display.active { color: #e85c23; }
    .agent-name-display.completed { color: #28a745; }

    /* Status text */
    .agent-status-text {
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        display: inline-block;
    }

    .agent-status-text.pending {
        background: #e9ecef;
        color: #6c757d;
    }

    .agent-status-text.active {
        background: #fff3cd;
        color: #856404;
    }

    .agent-status-text.completed {
        background: #d4edda;
        color: #155724;
    }

    /* Task chips */
    .agent-task-list {
        margin-top: 0.5rem;
        min-height: 30px;
    }

    .task-chip {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 5px;
        font-size: 0.65rem;
        margin: 0.15rem;
        font-weight: 500;
        background: #f8f9fa;
        color: #495057;
        border: 1px solid #dee2e6;
    }

    .task-chip.completed {
        background: #d4edda;
        color: #155724;
        border-color: #c3e6cb;
    }

    .task-chip.active {
        background: #fff3cd;
        color: #856404;
        border-color: #ffc107;
    }

    /* Time display */
    .agent-time-display {
        font-size: 0.65rem;
        color: #6c757d;
        margin-top: 0.5rem;
        padding: 0.3rem;
        background: #f8f9fa;
        border-radius: 5px;
    }

    /* Live status banner */
    .live-status-banner {
        background: #4B3C99;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .live-status-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .live-indicator {
        width: 8px;
        height: 8px;
        background: #28a745;
        border-radius: 50%;
        animation: blink 1.5s infinite;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    .live-status-text {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .live-status-agent {
        font-size: 1.1rem;
        font-weight: 600;
    }

    .live-status-progress {
        font-size: 0.85rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>&#9889; AEMplify</h1>
    <p>Transform UI Designs into AEM Components with AI-Powered Automation</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'crew_running' not in st.session_state:
    st.session_state.crew_running = False
if 'crew_started' not in st.session_state:
    st.session_state.crew_started = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'uploaded_image_path' not in st.session_state:
    st.session_state.uploaded_image_path = None
if 'log_monitor_thread' not in st.session_state:
    st.session_state.log_monitor_thread = None
if 'last_log_position' not in st.session_state:
    st.session_state.last_log_position = 0
if 'agent_status' not in st.session_state:
    st.session_state.agent_status = {
        'visual_strategist': {'status': 'pending', 'tasks': [], 'start_time': None, 'end_time': None},
        'ui_architect': {'status': 'pending', 'tasks': [], 'start_time': None, 'end_time': None},
        'aem_alchemist': {'status': 'pending', 'tasks': [], 'start_time': None, 'end_time': None}
    }
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = None
if 'task_progress' not in st.session_state:
    st.session_state.task_progress = []

# Sidebar - Configuration
with st.sidebar:
    st.markdown("### &#9881; Configuration")

    st.markdown("#### &#128193; Project Settings")
    output_folder = st.text_input(
        "Output Folder Base",
        value="output",
        help="Base folder name (agent folders will be created: output-visual_strategist, output-ui_architect, output-aem_alchemist)"
    )

    st.markdown("#### &#127919; AEM Settings")
    aem_project_path = st.text_input(
        "AEM Project Path",
        value="",
        placeholder="C:/path/to/aem/project",
        help="Full path to your AEM project root"
    )

    aem_app_id = st.text_input(
        "AEM App ID",
        value="myproject",
        help="Your AEM application ID (e.g., 'myproject')"
    )

    aem_namespace = st.text_input(
        "Java Namespace",
        value="com.mycompany",
        help="Java package namespace (e.g., 'com.mycompany')"
    )

    aem_component_group = st.text_input(
        "Component Group",
        value="My Project Components",
        help="Component group name in AEM"
    )

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### &#128248; Upload Design Image")

    uploaded_file = st.file_uploader(
        "Choose a design mockup or screenshot",
        type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
        help="Upload your UI design image (PNG, JPG, JPEG, GIF, WEBP)"
    )

    if uploaded_file is not None:
        # Save uploaded file as design.png (replace existing)
        filename = "design.png"
        filepath = Path(filename)

        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state.uploaded_image_path = str(filepath)

        # Professional compact image preview - thumbnail style
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; border: 1px solid #dee2e6; margin-top: 1rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="flex-shrink: 0;">
                    <div style="width: 80px; height: 80px; background: white; border-radius: 6px; border: 2px solid #dee2e6; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                        <span style="font-size: 2rem;">🖼️</span>
                    </div>
                </div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #28a745; margin-bottom: 0.25rem;">✓ Design Uploaded</div>
                    <div style="font-size: 0.9rem; color: #495057;">{uploaded_file.name}</div>
                    <div style="font-size: 0.8rem; color: #6c757d; margin-top: 0.25rem;">{uploaded_file.size / 1024:.1f} KB • {uploaded_file.type}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Optional: Show preview in expander for those who want to see it
        with st.expander("🔍 View Full Preview"):
            st.image(uploaded_file, use_container_width=True)

with col2:
    st.markdown("### &#128640; Crew Status")

    if st.session_state.crew_running:
        st.markdown('<p class="status-running">&#8987; Crew is running...</p>', unsafe_allow_html=True)
    elif st.session_state.uploaded_image_path:
        st.markdown('<p class="status-ready">&#9989; Ready to start</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p>&#128203; Waiting for design upload...</p>', unsafe_allow_html=True)

    # Start button
    start_button = st.button(
        "Start AEM Conversion",
        disabled=st.session_state.crew_running or not st.session_state.uploaded_image_path,
        use_container_width=True
    )

if start_button and st.session_state.uploaded_image_path:
    # Clean output folders before starting
    import shutil
    output_folders = ['output-visual_strategist', 'output-ui_architect', 'output-aem_alchemist']
    for folder in output_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.makedirs(folder, exist_ok=True)

    st.session_state.crew_running = True
    st.session_state.crew_started = True  # Mark that crew has been started
    st.session_state.logs = []
    # Reset agent status
    st.session_state.agent_status = {
        'visual_strategist': {'status': 'pending', 'tasks': [], 'start_time': None, 'end_time': None},
        'ui_architect': {'status': 'pending', 'tasks': [], 'start_time': None, 'end_time': None},
        'aem_alchemist': {'status': 'pending', 'tasks': [], 'start_time': None, 'end_time': None}
    }
    st.session_state.current_agent = None
    st.session_state.task_progress = []

    # Add initial log
    st.session_state.logs.append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "level": "info",
        "message": "🧹 Cleaned output folders"
    })
    st.session_state.logs.append({
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "level": "info",
        "message": "AEMplify starting..."
    })

    st.rerun()

# Function to render horizontal agent timeline
def render_agent_timeline():
    """Render the professional horizontal agent timeline"""

    agent_info = {
        'visual_strategist': {'name': 'Visual Strategist', 'icon': '&#128200;', 'number': '01'},  # 📈 Chart icon
        'ui_architect': {'name': 'UI Architect', 'icon': '&#128295;', 'number': '02'},  # 🔧 Wrench icon
        'aem_alchemist': {'name': 'AEM Alchemist', 'icon': '&#9889;', 'number': '03'}  # ⚡ Lightning icon
    }

    # Live status banner (if crew is running)
    if st.session_state.crew_running and st.session_state.current_agent:
        current_agent_info = agent_info.get(st.session_state.current_agent)
        current_tasks = st.session_state.agent_status[st.session_state.current_agent]['tasks']
        current_task = current_tasks[-1] if current_tasks else "Initializing..."

        st.markdown(f"""
        <div class="live-status-banner">
            <div class="live-status-left">
                <div class="live-indicator"></div>
                <div class="live-status-text">LIVE EXECUTION</div>
            </div>
            <div>
                <div class="live-status-agent">{current_agent_info['name']}</div>
                <div class="live-status-progress">{current_task}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Horizontal timeline
    timeline_html = '<div class="timeline-section">'
    timeline_html += '<div class="timeline-horizontal">'

    for agent_id in ['visual_strategist', 'ui_architect', 'aem_alchemist']:
        agent_data = st.session_state.agent_status[agent_id]
        status = agent_data['status']
        tasks = agent_data['tasks']
        info = agent_info[agent_id]

        # Agent column
        timeline_html += '<div class="agent-column">'

        # Icon container with status
        timeline_html += f'<div class="agent-icon-container {status}">'
        timeline_html += f'<span style="font-size: 2rem;">{info["icon"]}</span>'

        # Status badge with number or checkmark
        if status == 'completed':
            badge_content = '&#10003;'  # ✓
        elif status == 'active':
            badge_content = info['number']
        else:
            badge_content = info['number']

        timeline_html += f'<div class="agent-status-badge {status}">{badge_content}</div>'
        timeline_html += '</div>'

        # Agent name
        timeline_html += f'<div class="agent-name-display {status}">{info["name"]}</div>'

        # Status text
        if status == 'completed':
            status_text = 'COMPLETED'
        elif status == 'active':
            status_text = 'IN PROGRESS'
        else:
            status_text = 'PENDING'

        timeline_html += f'<div class="agent-status-text {status}">{status_text}</div>'

        # Tasks
        if tasks:
            timeline_html += '<div class="agent-task-list">'
            for task in tasks:
                task_status = 'completed' if status == 'completed' else ('active' if status == 'active' else 'pending')
                timeline_html += f'<span class="task-chip {task_status}">{task}</span>'
            timeline_html += '</div>'
        else:
            timeline_html += '<div class="agent-task-list"></div>'

        # Time info
        if agent_data['start_time']:
            start_str = agent_data['start_time'].strftime("%H:%M:%S")
            if agent_data['end_time']:
                end_str = agent_data['end_time'].strftime("%H:%M:%S")
                duration = (agent_data['end_time'] - agent_data['start_time']).seconds
                timeline_html += f'<div class="agent-time-display">Duration: {duration}s<br>{start_str} → {end_str}</div>'
            else:
                timeline_html += f'<div class="agent-time-display">Started: {start_str}</div>'

        # View Files button - only show if agent completed
        if status == 'completed':
            # Map agent to their output folder
            output_folders = {
                'visual_strategist': 'output-visual_strategist',
                'ui_architect': 'output-ui_architect',
                'aem_alchemist': 'output-aem_alchemist'
            }
            folder = output_folders.get(agent_id, '')
            timeline_html += f'''
            <div style="margin-top: 0.75rem;">
                <button onclick="window.viewAgentFiles('{agent_id}', '{folder}')"
                        style="background: #4B3C99; color: white; border: none; padding: 0.4rem 0.8rem;
                               border-radius: 6px; font-size: 0.7rem; cursor: pointer; font-weight: 600;
                               transition: all 0.2s;">
                    📁 View Files
                </button>
            </div>
            '''

        timeline_html += '</div>'  # Close agent-column

    timeline_html += '</div></div>'  # Close timeline-horizontal and timeline-section

    # Add JavaScript for handling file viewing
    timeline_html += '''
    <script>
    window.viewAgentFiles = function(agentId, folder) {
        // Create a custom event that Streamlit can listen to
        const event = new CustomEvent('viewFiles', {
            detail: { agentId: agentId, folder: folder }
        });
        window.dispatchEvent(event);

        // Show alert for now (can be replaced with modal)
        alert('📁 Files location: ' + folder + '\\n\\nCheck the folder in your project directory to view the created files.');
    }
    </script>
    '''

    st.markdown(timeline_html, unsafe_allow_html=True)

    # File viewer expanders for completed agents
    if st.session_state.agent_status['visual_strategist']['status'] == 'completed':
        with st.expander("📄 Visual Strategist Output - design_analysis.md"):
            try:
                with open('output-visual_strategist/design_analysis.md', 'r', encoding='utf-8') as f:
                    st.markdown(f.read())
            except:
                st.info("File not found yet")

    if st.session_state.agent_status['ui_architect']['status'] == 'completed':
        import os

        # Component Specification
        with st.expander("📋 Component Specification (component_list.md)"):
            try:
                spec_path = 'output-ui_architect/component_list.md'
                if os.path.exists(spec_path):
                    with open(spec_path, 'r', encoding='utf-8') as f:
                        st.markdown(f.read())
                else:
                    st.warning(f"File not found: {spec_path}")
            except Exception as e:
                st.error(f"Error reading specification: {str(e)}")

        # HTML Components - Each in separate expander with better error handling
        html_folder = 'output-ui_architect'

        if os.path.exists(html_folder):
            try:
                files = sorted([f for f in os.listdir(html_folder) if f.endswith('.html')])

                if files:
                    st.markdown("---")
                    st.markdown("### 📄 HTML Components")

                    # Use absolute file path as base for unique key to avoid any conflicts
                    for idx, file in enumerate(files):
                        # Get component name without extension for title
                        component_name = file.replace('.html', '').replace('-', ' ').title()

                        # Create absolutely unique key using full path + position + filename
                        # This guarantees uniqueness even if same filename exists elsewhere
                        import hashlib
                        absolute_path = os.path.abspath(os.path.join(html_folder, file))
                        unique_seed = f"{absolute_path}_{idx}_{id(file)}"
                        file_unique_id = hashlib.sha256(unique_seed.encode()).hexdigest()[:16]

                        with st.expander(f"📄 {component_name} ({file})", expanded=False):
                            file_path = os.path.join(html_folder, file)

                            if os.path.exists(file_path):
                                try:
                                    with open(file_path, 'r', encoding='utf-8') as f:
                                        code_content = f.read()

                                    # View mode toggle with unique key per component
                                    col1, col2 = st.columns([3, 1])
                                    with col1:
                                        view_mode = st.radio(
                                            "View Mode:",
                                            ["🖼️ Preview", "💻 Source"],
                                            horizontal=True,
                                            key=f"vm_{file_unique_id}",
                                            label_visibility="collapsed",
                                            index=0
                                        )
                                    with col2:
                                        # Download button
                                        st.download_button(
                                            label="⬇️ Download",
                                            data=code_content,
                                            file_name=file,
                                            mime='text/html',
                                            key=f"dl_{file_unique_id}",
                                            use_container_width=True
                                        )

                                    st.markdown("---")

                                    if view_mode == "🖼️ Preview":
                                        # Render HTML in iframe for isolated viewing
                                        st.markdown("**🖼️ Live Preview:**")
                                        import streamlit.components.v1 as components
                                        components.html(code_content, height=600, scrolling=True)
                                    else:
                                        # Show source code
                                        st.markdown("**💻 HTML Source:**")
                                        st.code(code_content, language='html', line_numbers=True)

                                except Exception as e:
                                    st.error(f"Error reading {file}: {str(e)}")
                            else:
                                st.error(f"File disappeared: {file_path}")
                else:
                    st.info("⏳ No HTML components created yet. UI Architect is still working...")

            except Exception as e:
                st.error(f"Error scanning HTML folder: {str(e)}")
        else:
            st.info(f"📁 Output folder not created yet: {html_folder}")

    if st.session_state.agent_status['aem_alchemist']['status'] == 'completed':
        with st.expander("📄 AEM Alchemist Output - AEM Files"):
            st.info("AEM files created in your project directory. Check the logs for file paths.")

# ========================================
# TIMELINE SECTION (Shows above logs) - Dynamic placeholder
# ========================================
st.markdown("---")
timeline_placeholder = st.empty()

# Render timeline if crew has started
if st.session_state.crew_started:
    with timeline_placeholder.container():
        render_agent_timeline()

# ========================================
# LOGS SECTION
# ========================================
st.markdown("---")
st.markdown("### &#128203; Execution Logs")

# Log container
log_placeholder = st.empty()

# Function to strip ANSI color codes
def strip_ansi_codes(text):
    """Remove ANSI color/formatting codes from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# Function to detect and update agent/task status from logs
def update_agent_status_from_log(line):
    """Detect agent and task changes from log lines and update status - EXPERT MODE"""

    # Define agent and task mapping based on actual crew configuration
    agent_task_mapping = {
        'visual_strategist': ['Design Analysis'],
        'ui_architect': ['Component Listing', 'Component Creation'],
        'aem_alchemist': ['AEM Selection', 'AEM Conversion', 'Build & Deploy', 'Testing']
    }

    agent_order = ['visual_strategist', 'ui_architect', 'aem_alchemist']

    # ========== AGENT DETECTION ==========
    # Multiple patterns to catch agent activation in CrewAI logs

    # Pattern 1: "Working Agent: <role>" - Most reliable
    if "Working Agent:" in line:
        if "Visual Strategist" in line:
            activate_agent('visual_strategist')
        elif "UI Architect" in line:
            activate_agent('ui_architect')
        elif "AEM Alchemist" in line:
            activate_agent('aem_alchemist')

    # Pattern 2: "# Agent: <role>" - Markdown header in logs
    elif "# Agent:" in line:
        if "Visual Strategist" in line:
            activate_agent('visual_strategist')
        elif "UI Architect" in line:
            activate_agent('ui_architect')
        elif "AEM Alchemist" in line:
            activate_agent('aem_alchemist')

    # Pattern 3: Agent name in brackets [Agent: role]
    elif "[Agent:" in line or "Agent:" in line:
        if "Visual Strategist" in line:
            activate_agent('visual_strategist')
        elif "UI Architect" in line:
            activate_agent('ui_architect')
        elif "AEM Alchemist" in line:
            activate_agent('aem_alchemist')

    # Pattern 4: "Entering new" chain with agent context
    elif "Entering new" in line and "chain" in line:
        # This indicates an agent is starting work
        # Need to infer from previous context or next lines
        pass

    # Pattern 5: Task-based agent detection (fallback)
    elif "## Task:" in line or "Task Description:" in line or "Starting Task:" in line:
        # Detect which agent should be active based on task name
        if "design_analysis" in line.lower():
            activate_agent('visual_strategist')
        elif "component_listing" in line.lower() or "component_creation" in line.lower():
            activate_agent('ui_architect')
        elif "aem_component" in line.lower() or "aem_build" in line.lower() or "aem_testing" in line.lower():
            activate_agent('aem_alchemist')

    # Pattern 6: Output file detection (very reliable)
    elif "output-visual_strategist" in line:
        activate_agent('visual_strategist')
    elif "output-ui_architect" in line:
        activate_agent('ui_architect')
    elif "output-aem_alchemist" in line:
        activate_agent('aem_alchemist')

    # ========== TASK DETECTION - ACTUAL OUTPUTS ==========
    current = st.session_state.current_agent

    # Detect actual component/file creation for each agent
    if current:
        task_detected = None

        # Visual Strategist outputs
        if current == 'visual_strategist':
            if "design_analysis" in line.lower() or "saved to output-visual_strategist" in line.lower():
                task_detected = "Design Analysis"

        # UI Architect outputs - detect actual component files created
        elif current == 'ui_architect':
            # Detect component list creation
            if "component_list" in line.lower() or "component specification" in line.lower():
                if "Component Spec" not in st.session_state.agent_status[current]['tasks']:
                    task_detected = "Component Spec"

            # Detect actual HTML component creation (navbar.html, hero.html, etc.)
            if ".html" in line and ("created" in line.lower() or "saved" in line.lower() or "writing" in line.lower()):
                # Extract component name from line (e.g., "navbar.html" -> "navbar")
                import re
                match = re.search(r'(\w+[-\w]*).html', line)
                if match:
                    component_name = match.group(1)
                    task_detected = component_name

        # AEM Alchemist outputs
        elif current == 'aem_alchemist':
            # Detect component selection
            if "aem_component_selection" in line.lower() or "component to convert" in line.lower():
                if "Component Selection" not in st.session_state.agent_status[current]['tasks']:
                    task_detected = "Selection"

            # Detect AEM files created
            elif ".content.xml" in line or "sling model" in line.lower() or "htl template" in line.lower():
                if "AEM Component" not in st.session_state.agent_status[current]['tasks']:
                    task_detected = "AEM Component"

            # Detect Maven build
            elif "mvn clean install" in line.lower() or "build success" in line.lower():
                if "Build" not in st.session_state.agent_status[current]['tasks']:
                    task_detected = "Build"

            # Detect testing
            elif "testing" in line.lower() or "aem_testing_report" in line.lower():
                if "Testing" not in st.session_state.agent_status[current]['tasks']:
                    task_detected = "Testing"

        # Add task if detected and not already present
        if task_detected and task_detected not in st.session_state.agent_status[current]['tasks']:
            st.session_state.agent_status[current]['tasks'].append(task_detected)

    # ========== COMPLETION DETECTION ==========
    # Detect when tasks/agents finish

    # Pattern 1: Task completion indicators
    if any(pattern in line for pattern in ["Finished chain", "Final Answer:", "Task output saved"]):
        # A task just completed
        if current:
            # Add completion marker to current task
            pass

    # Pattern 2: Agent switching indicates previous agent completed
    # This is already handled in activate_agent() function

    # Pattern 3: Specific task completion patterns
    if "design_analysis" in line and "saved" in line.lower():
        # Visual Strategist completed
        mark_agent_complete('visual_strategist')
    elif "component_summary.txt" in line and "saved" in line.lower():
        # UI Architect completed both tasks
        mark_agent_complete('ui_architect')
    elif "aem_testing_report.txt" in line and "saved" in line.lower():
        # AEM Alchemist completed all tasks
        mark_agent_complete('aem_alchemist')

def mark_agent_complete(agent_id):
    """Helper function to mark an agent as completed"""
    if agent_id in st.session_state.agent_status:
        if st.session_state.agent_status[agent_id]['status'] == 'active':
            st.session_state.agent_status[agent_id]['status'] = 'completed'
            if not st.session_state.agent_status[agent_id]['end_time']:
                st.session_state.agent_status[agent_id]['end_time'] = datetime.now()

def activate_agent(agent_id):
    """Helper function to activate an agent and update status"""
    if agent_id not in st.session_state.agent_status:
        return

    # Skip if already completed
    if st.session_state.agent_status[agent_id]['status'] == 'completed':
        return

    agent_order = ['visual_strategist', 'ui_architect', 'aem_alchemist']
    agent_names = {
        'visual_strategist': 'Visual Strategist',
        'ui_architect': 'UI Architect',
        'aem_alchemist': 'AEM Alchemist'
    }

    # Mark all previous agents as completed
    current_index = agent_order.index(agent_id)
    for i in range(current_index):
        prev_agent = agent_order[i]
        if st.session_state.agent_status[prev_agent]['status'] != 'completed':
            st.session_state.agent_status[prev_agent]['status'] = 'completed'
            if not st.session_state.agent_status[prev_agent]['end_time']:
                st.session_state.agent_status[prev_agent]['end_time'] = datetime.now()
            # Log the completion
            print(f"[STATUS] {agent_names[prev_agent]} completed")

    # Activate current agent
    if st.session_state.agent_status[agent_id]['status'] != 'completed':
        st.session_state.agent_status[agent_id]['status'] = 'active'
        if not st.session_state.agent_status[agent_id]['start_time']:
            st.session_state.agent_status[agent_id]['start_time'] = datetime.now()
        st.session_state.current_agent = agent_id
        # Log the activation
        print(f"[STATUS] {agent_names[agent_id]} activated")

# Function to filter and clean log lines for professional display
def is_relevant_log(line):
    """Determine if a log line should be displayed to user"""

    # Skip empty lines
    if not line:
        return False

    # Skip repetitive CrewAI internal messages
    skip_patterns = [
        # "Working Agent:",  # NOW KEPT - we use this for status tracking
        # "Starting Task:",  # NOW KEPT - we use this for status tracking
        "[DEBUG]",  # Debug level logs
        "Entering new CrewAgentExecutor chain",  # Internal framework details
        "# Agent:",  # Markdown headers that don't add value
        "## Task:",  # Markdown headers that don't add value
        "Thought: Do I need to use a tool?",  # Repetitive thinking patterns
        "Action Input:",  # Tool input details (too verbose)
        "Observation:",  # Tool observation prefix (redundant)
    ]

    for pattern in skip_patterns:
        if pattern in line:
            return False

    # Keep important log types
    keep_patterns = [
        "[Agent:",  # Agent actions
        "[Tool:",  # Tool usage
        "✓",  # Success indicators
        "✗",  # Failure indicators
        "ERROR",  # Errors
        "Error",  # Errors
        "WARNING",  # Warnings
        "Created",  # File/folder creation
        "Saved",  # File saves
        "Executing",  # Command execution
        "Analyzing",  # Analysis steps
        "Converting",  # Conversion steps
        "Building",  # Build steps
        "Testing",  # Test steps
        "Final Answer:",  # Agent conclusions
    ]

    for pattern in keep_patterns:
        if pattern in line:
            return True

    # Keep lines that look like actual content (not metadata)
    # Skip lines that are just decorative (borders, separators)
    if line.strip() in ["", "─", "│", "┌", "┐", "└", "┘", "═", "║", "╔", "╗", "╚", "╝"]:
        return False

    if all(c in "─│┌┐└┘═║╔╗╚╝-_=*#" for c in line.strip()):
        return False

    # Keep lines that have substantial content
    if len(line.strip()) > 20:
        return True

    return False

# Function to read new logs from file
def read_new_logs():
    """Read new logs from file since last position"""
    if not os.path.exists(log_file):
        return []

    new_logs = []
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            f.seek(st.session_state.last_log_position)
            new_lines = f.readlines()
            st.session_state.last_log_position = f.tell()

            for line in new_lines:
                # Strip ANSI codes first
                line = strip_ansi_codes(line).strip()

                # Update agent status from this log line
                update_agent_status_from_log(line)

                # Filter out irrelevant logs
                if not is_relevant_log(line):
                    continue

                if line:
                    # Parse log level from line
                    level = "info"
                    if "ERROR" in line or "Error" in line or "✗" in line:
                        level = "error"
                    elif "WARNING" in line or "Warning" in line:
                        level = "warning"
                    elif "SUCCESS" in line or "success" in line or "✓" in line or "Final Answer:" in line:
                        level = "success"

                    new_logs.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "level": level,
                        "message": line
                    })
    except Exception as e:
        pass

    return new_logs

# Function to update log display
def update_log_display():
    """Update the log display in UI"""
    log_html = '<div class="log-container">'
    for log in st.session_state.logs:
        level_class = f"log-{log['level']}"
        log_html += f'<div class="log-entry {level_class}">[{log["timestamp"]}] {log["message"]}</div>'
    log_html += '</div>'
    log_placeholder.markdown(log_html, unsafe_allow_html=True)

# Run crew if started
if st.session_state.crew_running:
    try:
        # Add initial logs
        st.session_state.logs.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": "info",
            "message": f"Design image: {st.session_state.uploaded_image_path}"
        })
        st.session_state.logs.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": "info",
            "message": f"Output folder: {output_folder}"
        })
        st.session_state.logs.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": "info",
            "message": "Initializing crew agents..."
        })

        # Update logs display
        update_log_display()

        # Create crew instance
        crew = DevAemCrewSys()

        # Prepare inputs
        inputs = {
            'design_path': st.session_state.uploaded_image_path,
            'output_folder': output_folder,
            'aem_project_path': aem_project_path,
            'aem_app_id': aem_app_id,
            'aem_namespace': aem_namespace,
            'aem_component_group': aem_component_group,
            'selected_component': 'navbar',  # Default to navbar, will be updated by agent
            'component_name': 'navbar'  # Default to navbar, will be updated by agent
        }

        st.session_state.logs.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": "success",
            "message": "Crew initialized successfully"
        })
        st.session_state.logs.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": "info",
            "message": "Starting crew execution... (This may take a few minutes)"
        })

        # Update logs
        update_log_display()

        # Clear log file before starting
        with open(log_file, 'w') as f:
            f.write("")
        st.session_state.last_log_position = 0

        # Function to run crew in background thread
        crew_result = {"result": None, "error": None, "completed": False}

        def run_crew():
            try:
                # Capture stdout and stderr to log file
                class LogCapture:
                    def __init__(self, file_handle, terminal):
                        self.file_handle = file_handle
                        self.terminal = terminal

                    def write(self, message):
                        # Write to both file and terminal
                        self.file_handle.write(message)
                        self.file_handle.flush()
                        if self.terminal:
                            self.terminal.write(message)

                    def flush(self):
                        self.file_handle.flush()
                        if self.terminal:
                            self.terminal.flush()

                # Redirect stdout and stderr to capture all output
                with open(log_file, 'a', encoding='utf-8') as log_f:
                    old_stdout = sys.stdout
                    old_stderr = sys.stderr

                    log_capture_stdout = LogCapture(log_f, old_stdout)
                    log_capture_stderr = LogCapture(log_f, old_stderr)

                    try:
                        sys.stdout = log_capture_stdout
                        sys.stderr = log_capture_stderr

                        # Run the crew
                        crew_result["result"] = crew.crew().kickoff(inputs=inputs)
                    finally:
                        sys.stdout = old_stdout
                        sys.stderr = old_stderr

                crew_result["completed"] = True
            except Exception as e:
                crew_result["error"] = str(e)
                crew_result["completed"] = True

        # Start crew in background thread
        crew_thread = threading.Thread(target=run_crew, daemon=True)
        crew_thread.start()

        # Monitor logs while crew is running
        progress_bar = st.progress(0)
        status_text = st.empty()

        log_check_interval = 0.5  # Check for new logs every 0.5 seconds
        max_wait_time = 600  # Maximum 10 minutes
        elapsed_time = 0

        while not crew_result["completed"] and elapsed_time < max_wait_time:
            # Read new logs
            new_logs = read_new_logs()
            if new_logs:
                st.session_state.logs.extend(new_logs)
                update_log_display()

                # Re-render timeline to show updated agent status
                with timeline_placeholder.container():
                    render_agent_timeline()

            # Update progress
            progress = min(elapsed_time / max_wait_time, 0.99)
            progress_bar.progress(progress)

            # Show current agent in status
            current_agent_name = "Starting..."
            if st.session_state.current_agent:
                agent_names_map = {
                    'visual_strategist': 'Visual Strategist',
                    'ui_architect': 'UI Architect',
                    'aem_alchemist': 'AEM Alchemist'
                }
                current_agent_name = agent_names_map.get(st.session_state.current_agent, "Working...")

            status_text.text(f"🤖 {current_agent_name} - {int(elapsed_time)}s elapsed")

            time.sleep(log_check_interval)
            elapsed_time += log_check_interval

        # Wait for thread to complete
        crew_thread.join(timeout=5)

        # Final log read
        new_logs = read_new_logs()
        if new_logs:
            st.session_state.logs.extend(new_logs)

        progress_bar.progress(1.0)
        status_text.empty()

        # Check for errors
        if crew_result["error"]:
            raise Exception(crew_result["error"])

        result = crew_result["result"]

        # Success
        st.session_state.logs.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": "success",
            "message": "✓ Crew execution completed successfully!"
        })
        st.session_state.logs.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": "info",
            "message": f"Result: {str(result)[:200]}..."
        })
        st.session_state.logs.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": "success",
            "message": "✓ Process finished - Check output folder for generated files"
        })

        # Update final logs
        update_log_display()

        st.success("✅ Conversion completed successfully!")

    except Exception as e:
        st.session_state.logs.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "level": "error",
            "message": f"❌ Error: {str(e)}"
        })
        st.error(f"Error: {str(e)}")

        # Update error logs
        update_log_display()

    finally:
        st.session_state.crew_running = False
        st.rerun()

# Display logs if not running (running logs are handled above)
if not st.session_state.crew_running:
    if st.session_state.logs:
        update_log_display()
    else:
        log_placeholder.info("Logs will appear here when you start the conversion...")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>AEMplify</strong> - Powered by CrewAI & Claude AI</p>
    <p>Design Analysis &#8594; HTML Components &#8594; AEM Conversion</p>
</div>
""", unsafe_allow_html=True)

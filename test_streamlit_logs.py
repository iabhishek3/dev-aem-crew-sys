"""
Test script to verify real-time log streaming works correctly
Run this with: streamlit run test_streamlit_logs.py
"""
import streamlit as st
import time
import threading
import os
from datetime import datetime

st.set_page_config(page_title="Log Streaming Test", layout="wide")

st.title("🧪 Real-Time Log Streaming Test")

# Initialize session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'last_log_position' not in st.session_state:
    st.session_state.last_log_position = 0

log_file = "test_log.txt"

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
                line = line.strip()
                if line:
                    new_logs.append({
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "message": line
                    })
    except Exception as e:
        st.error(f"Error reading logs: {e}")

    return new_logs

def update_log_display(placeholder):
    """Update the log display"""
    if st.session_state.logs:
        log_text = "\n".join([f"[{log['timestamp']}] {log['message']}" for log in st.session_state.logs])
        placeholder.code(log_text, language="log")
    else:
        placeholder.info("No logs yet...")

# Test function that simulates CrewAI
def simulate_crew_execution():
    """Simulates a crew execution with logs"""
    import sys

    class LogCapture:
        def __init__(self, file_handle, terminal):
            self.file_handle = file_handle
            self.terminal = terminal

        def write(self, message):
            self.file_handle.write(message)
            self.file_handle.flush()
            if self.terminal:
                self.terminal.write(message)

        def flush(self):
            self.file_handle.flush()
            if self.terminal:
                self.terminal.flush()

    with open(log_file, 'a', encoding='utf-8') as log_f:
        old_stdout = sys.stdout

        log_capture = LogCapture(log_f, old_stdout)

        try:
            sys.stdout = log_capture

            # Simulate crew work
            print("Starting crew execution...")
            time.sleep(1)

            print("[Agent: Designer] Analyzing image...")
            time.sleep(2)

            print("[Agent: Designer] Found 5 components")
            time.sleep(1)

            print("[Agent: Developer] Creating navbar component...")
            time.sleep(2)

            print("[Agent: Developer] Writing HTML file...")
            time.sleep(1)

            print("[Agent: Developer] Component created successfully")
            time.sleep(1)

            print("[Agent: AEM] Converting to AEM format...")
            time.sleep(2)

            print("[Agent: AEM] Running Maven build...")
            time.sleep(1)

            print("Crew execution completed!")

        finally:
            sys.stdout = old_stdout

# Main UI
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Test Controls")

    if st.button("Start Test", disabled=st.session_state.running):
        st.session_state.running = True
        st.session_state.logs = []
        st.session_state.last_log_position = 0

        # Clear log file
        with open(log_file, 'w') as f:
            f.write("")

        st.rerun()

with col2:
    st.markdown("### Status")
    if st.session_state.running:
        st.success("🟢 Running")
    else:
        st.info("⚪ Idle")

# Log display
st.markdown("---")
st.markdown("### 📋 Execution Logs")
log_placeholder = st.empty()

# Run test if started
if st.session_state.running:
    result = {"completed": False}

    def run_test():
        simulate_crew_execution()
        result["completed"] = True

    # Start background thread
    thread = threading.Thread(target=run_test, daemon=True)
    thread.start()

    # Monitor logs
    progress_bar = st.progress(0)
    status_text = st.empty()

    max_time = 20  # 20 seconds max
    elapsed = 0
    interval = 0.5

    while not result["completed"] and elapsed < max_time:
        # Read new logs
        new_logs = read_new_logs()
        if new_logs:
            st.session_state.logs.extend(new_logs)
            update_log_display(log_placeholder)

        # Update progress
        progress = min(elapsed / max_time, 0.99)
        progress_bar.progress(progress)
        status_text.text(f"Running... ({int(elapsed)}s)")

        time.sleep(interval)
        elapsed += interval

    # Wait for completion
    thread.join(timeout=2)

    # Final log read
    new_logs = read_new_logs()
    if new_logs:
        st.session_state.logs.extend(new_logs)

    progress_bar.progress(1.0)
    status_text.empty()

    update_log_display(log_placeholder)

    st.session_state.running = False
    st.success("✅ Test completed!")
    st.rerun()

else:
    # Display existing logs
    update_log_display(log_placeholder)

# Footer
st.markdown("---")
st.info("""
**Test Instructions:**
1. Click 'Start Test' button
2. Watch logs appear in real-time
3. Verify all messages are captured
4. Check for smooth updates

If logs appear in real-time, the implementation works! ✅
""")

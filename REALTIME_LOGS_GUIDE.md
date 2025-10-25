# Real-Time CrewAI Logs in Streamlit UI

## Overview
This guide explains how to capture and display all CrewAI execution logs in real-time on your Streamlit UI.

## What Was Changed

### 1. Added Required Imports (app.py:9-10)
```python
import threading
import time
```
These enable background thread execution and log polling.

### 2. Custom Log Handler (app.py:26-37)
Created `StreamlitLogHandler` class to capture Python logging events directly into the session state logs list.

### 3. Session State Variables (app.py:190-193)
Added tracking for:
- `log_monitor_thread`: Background thread reference
- `last_log_position`: File position tracker for incremental log reading

### 4. Log Reading Functions (app.py:312-354)

#### `read_new_logs()`
- Reads new log entries from `crew_execution.log` since last position
- Parses log levels (ERROR, WARNING, SUCCESS, INFO)
- Returns list of new log entries
- Uses file seek to only read new content

#### `update_log_display()`
- Renders logs in the UI with proper styling
- Color-codes logs based on level (error=red, success=green, etc.)
- Updates the log container in real-time

### 5. Background Crew Execution (app.py:416-453)

#### Key Features:
- **Thread-based execution**: Crew runs in background thread
- **stdout/stderr capture**: Custom `LogCapture` class redirects all print statements to log file
- **Real-time writing**: Logs flush immediately to file for instant visibility
- **Error handling**: Captures exceptions and stores in result dictionary

#### How It Works:
```python
def run_crew():
    # Captures ALL stdout/stderr output from CrewAI
    class LogCapture:
        def write(self, message):
            # Write to file AND terminal
            self.file_handle.write(message)
            self.file_handle.flush()

    # Redirect output
    sys.stdout = log_capture
    sys.stderr = log_capture

    # Run crew (all output captured)
    crew_result["result"] = crew.crew().kickoff(inputs=inputs)
```

### 6. Log Monitoring Loop (app.py:458-449)

```python
while not crew_result["completed"]:
    # Read new logs every 0.5 seconds
    new_logs = read_new_logs()
    if new_logs:
        st.session_state.logs.extend(new_logs)
        update_log_display()

    # Update progress bar
    progress_bar.progress(progress)
    time.sleep(0.5)
```

## How It Works - Complete Flow

### 1. User Clicks "Start AEM Conversion"
   - Session state updated to `crew_running = True`
   - Log file cleared and position reset

### 2. Crew Thread Starts
   - Background thread created with `run_crew()` function
   - stdout/stderr redirected to log file
   - CrewAI execution begins

### 3. Real-Time Monitoring
   - Main thread polls log file every 0.5 seconds
   - New log lines parsed and added to UI
   - Progress bar updates with elapsed time
   - User sees live agent activity

### 4. Completion
   - Thread completes execution
   - Final logs read and displayed
   - Success/error message shown
   - Session state reset

## What Logs Are Captured

### ✅ All CrewAI Output:
- Agent thinking process
- Task execution steps
- Tool usage (VisionTool, FileWriterTool, etc.)
- LLM API calls
- Agent collaboration
- Task results
- Error messages
- Warnings

### ✅ Custom Application Logs:
- Initialization messages
- Configuration details
- Progress updates
- Completion status

## Benefits

1. **Real-Time Visibility**: See exactly what agents are doing
2. **Debugging**: Identify where issues occur during execution
3. **User Experience**: Users aren't left wondering what's happening
4. **Progress Tracking**: Know which task/agent is active
5. **Error Detection**: Immediately see errors as they happen

## Configuration Options

### Adjust Log Polling Interval (app.py:432)
```python
log_check_interval = 0.5  # Check every 0.5 seconds
```
- Lower = more responsive, higher CPU usage
- Higher = less responsive, lower CPU usage

### Change Maximum Wait Time (app.py:433)
```python
max_wait_time = 600  # 10 minutes maximum
```

### Customize Log Styling (app.py:84-105)
Modify CSS classes in the `<style>` section:
- `.log-info` - Info messages (cyan)
- `.log-success` - Success messages (green)
- `.log-warning` - Warnings (orange)
- `.log-error` - Errors (red)

## Troubleshooting

### Logs Not Appearing?

1. **Check verbose mode** in crew.py:
   ```python
   verbose=True  # Should be enabled for all agents
   ```

2. **Verify log file permissions**:
   - Ensure app can write to `crew_execution.log`

3. **Check file encoding**:
   - Log file opened with `encoding='utf-8'`

### Performance Issues?

1. **Increase polling interval**:
   ```python
   log_check_interval = 1.0  # Slower polling
   ```

2. **Limit log history**:
   ```python
   # Keep only last 1000 log entries
   if len(st.session_state.logs) > 1000:
       st.session_state.logs = st.session_state.logs[-1000:]
   ```

### Logs Cut Off?

Check the `max_wait_time` setting - increase if crew takes longer than 10 minutes.

## Next Steps

### Enhanced Features You Could Add:

1. **Log Filtering**: Filter by agent or log level
2. **Download Logs**: Export button for full log file
3. **Log Search**: Search functionality for specific messages
4. **Agent Status Panel**: Separate status indicators per agent
5. **Timestamp Filtering**: Show only recent logs
6. **Auto-scroll**: Keep latest log visible

## Example Output

```
[14:23:45] AEMplify starting...
[14:23:46] Design image: design.png
[14:23:46] Output folder: output
[14:23:46] Initializing crew agents...
[14:23:48] ✓ Crew initialized successfully
[14:23:48] Starting crew execution... (This may take a few minutes)
[14:23:50] [Agent: webdesigner] Analyzing design image...
[14:23:55] [Agent: webdesigner] Identified 5 components
[14:24:02] [Agent: component_developer] Creating navbar component...
[14:24:15] [Agent: component_developer] HTML file saved: output/navbar.html
[14:24:20] [Agent: aem_developer] Converting to AEM component...
[14:24:35] ✓ Crew execution completed successfully!
```

## Technical Notes

- **Thread Safety**: Uses dictionary for result sharing between threads
- **File Locking**: Sequential reads prevent conflicts
- **Memory Management**: Logs stored in session state (cleared on restart)
- **Encoding**: UTF-8 encoding prevents character issues
- **Buffering**: Flush calls ensure immediate writes

## Support

If logs still aren't appearing:
1. Check Python version (3.8+)
2. Verify Streamlit version (1.28+)
3. Ensure CrewAI verbose mode enabled
4. Check console for Python errors
5. Verify file permissions on working directory

# FPL Project V2

<img src="https://logodownload.org/wp-content/uploads/2016/03/premier-league-5.png" width="200" height="200">

## About

This project empowers Fantasy Premier League (FPL) enthusiasts by providing smarter, cheaper player alternatives for each gameweek. By leveraging insights from the FPL API, users can make more informed decisions to enhance their team strategy. Whether you're a seasoned player or new to FPL, this tool simplifies the process of analyzing and optimizing your lineup.

## Features

- **Comprehensive Analysis**: Evaluate all Premier League players with detailed metrics.
- **Smart Alternatives**: Identify cheaper, high-performing player substitutes.
- **Automated Reports**: Generate detailed gameweek insights tailored to your team.
- **Scheduled Notifications**: Automatically email reports for timely updates.
- **User-Friendly Frontend (Coming Soon)**: A planned interface to make the tool accessible to everyone.

## Development Status

Initially built as a personal project, this tool is evolving to include a user-friendly front end and expanded functionalities. If you'd like to replicate or enhance the project, step-by-step guidance is provided below.

## Setup Instructions

### 1. Fetching Data from the FPL API

Leverage the following API endpoints to gather data:

#### Main API:

`https://fantasy.premierleague.com/api/bootstrap-static/`

This endpoint provides comprehensive information on the Premier League, including player stats within the elements array.

#### Your Team API:

`https://fantasy.premierleague.com/api/entry/{your_team_key}/event/{current_gameweek}/picks/`

Replace `{your_team_key}` with your unique team ID and `{current_gameweek}` with the current gameweek number to access your lineup.

Organize and store this data in arrays or data structures for easy access. For example, separate all Premier League players from your current team to streamline further analysis.

### 2. Evaluating Cheaper Player Alternatives

Using metrics such as form (player performance) and now_cost (current price), identify budget-friendly players who outperform your current picks. This step helps you maximize your team's potential without exceeding budget constraints. Structure your data effectively to make it easy to match current players with their alternatives.

### 3. Generating Reports

Create a gameweek-specific report summarizing your findings:

- Include each player's name and their suggested alternative.
- Save the file with a consistent naming format, such as `Gameweek_{current_gameweek}.txt`, to maintain organization.

This report can be used for quick reference or shared with others.

### 4. Emailing Reports

Set up an email function to automate the delivery of gameweek reports. Use a reliable email service with SMTP integration to ensure the process is secure and efficient. Test this function thoroughly before deploying.

### 5. Scheduling the Script

Automate script execution using macOS's launchd utility. Follow these steps:

#### Create a .plist File

Place the file in `~/Library/LaunchAgents`. Replace placeholders with appropriate values:
In this example I have this automated to send me an email every Monday at 10AM but you can change it to your liking

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>com.yourusername.fplscript</string>
    <key>ProgramArguments</key>
    <array>
      <string>{path_to_python_interpreter}</string>
      <string>{path_to_script}</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
      <key>Hour</key>
      <integer>10</integer>
      <key>Minute</key>
      <integer>0</integer>
      <key>Weekday</key>
      <integer>1</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{path_to_output_log}</string>
    <key>StandardErrorPath</key>
    <string>{path_to_error_log}</string>
    <key>WorkingDirectory</key>
    <string>{path_to_working_directory}</string>
  </dict>
</plist>
```

#### Loading the Script

After creating the plist file you have to load the file for it to run at it's scheduled time

```
launchctl load ~/Library/LaunchAgents/com.yourusername.fplscript.plist
```

In case you decide to change your plist file make sure after to unload the plist file and then load up the new file

```
launchctl unload ~/Library/LaunchAgents/com.yourusername.fplscript.plist
```

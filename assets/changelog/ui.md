## [0.3.0-alpha.1] - 2026-11-14

The first pre-release of 0.3.0, built on oxrok `0.3.0-alpha.1`. Triggers are set on the channel rows and can use everything the device's trigger takes, missing firmware is downloaded from the app, and boards on USB serial ports are found without typing a connection string.

### Triggers

- **Trigger icons on the channel rows.** Every digital channel has a trigger icon next to its label. A click cycles it: none, rising, falling, either edge, high, low. Setting one switches the capture to Trigger mode.
- **Stages.** A device with two trigger stages shows two columns, A and B, with the letter on each set icon.
- **A Trigger tab.** The Inspector has a Trigger tab between Device and Analyze, opened by a right click on an icon or a click on a column letter. It shows the trigger in words, who waits for it (the device or the app), the capture durations before and after it, and what an icon cannot say: A then B, A or B, A and B; a count, with consecutive matches; a hold time or a pulse width (longer, shorter, between); a value range over several channels. A control the device cannot take is greyed, with the reason. While a capture runs the tab is read-only.
- **The device's own trigger on streaming devices.** When the device can take the whole trigger (fx2lafw, the Pico, the demo device), it waits for it and the capture is sized from the times before and after the trigger. Otherwise the app searches the recording, as before.
- **A trigger that cannot be used says so.** When the device rounds the sample rate and a pulse width no longer fits a whole sample, the start fails with the reason and the rate, where the capture used to begin without its trigger.
- **The time before the trigger is kept.** The memory buffer no longer trims it away at high sample rates, the device takes that much data before it arms the trigger, and Start warns when the buffer is too small for it.
- **Capture mode in the toolbar.** Trigger, Timed and Continuous are picked from a dropdown next to Repeat.
- **A faster search.** The app's trigger search is one pass over the edges: 64 Mi samples of a 6 MHz clock take 0.13 s, where they took 6.4 s.
- Sessions and settings saved by 0.2.0 load with their trigger.

### Devices

- **Install firmware.** When a device misses its firmware the app names the package, downloads it, checks it against pinned hashes and installs it; or takes the vendor's installer, an archive or a folder dropped on the dialog. An error about a missing file has an *Install…* button.
- **Boards on USB serial ports.** A Raspberry Pi Pico is recognised by its USB id and the app asks before it opens the port. A board that was accepted connects by itself the next time, on whatever port it appears. Other serial devices are not opened.
- A connected serial device is no longer reset by every rescan, and a port that cannot be opened says why.
- **Imported files** (VCD, CSV, `.sr`) have no device, so they no longer offer to record.

### Also

- Spanish and Simplified Chinese translations of the whole interface.
- macOS: the app is signed and carries the `oxrok` command line.
- The Command line panel writes stages, counts, pulse widths and ranges in oxrok's `-t` grammar.

### Known issues

- The new trigger paths were tested on the demo device and the mock, not yet on hardware: two stages and counts on an fx2lafw analyzer, the LogicPort, and the Pico's connection prompt.
- An fx2lafw analyzer offers 48 MS/s, which most of them cannot sustain over USB; 24 MS/s works.
- When the Pico aborts a capture (an analog rate it cannot reach, for one) the error does not say why.

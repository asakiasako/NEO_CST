# Changelog

All notable changes to this project will be documented in this file.

## [0.2.23] - 2021-12-17

- Fix bugs of test suite: All Channel Test

## [0.2.22] - 2021-12-15

- Fix test suite: All Channel Test

## [0.2.21] - 2021-11-24

### Changed

- Extend gRPC max_message_size from 4 MB to 10 MB.
- When load test data to GUI display, 'data' field is not transferred.

## [0.2.20] - 2021-11-19

### Added

- Add new test suite: All Channel Test

## [0.2.19] - 2021-11-17

### Added

- Support for POLC: ESP1000

## [0.2.18] - 2021-11-04

### Fixed

- Laser Center Frequency Accuracy: VOA unit fixed
- Recovered changes made in 0.2.15 about test cases:
  - Tx In-Band OSNR
  - Tx Out-of-Band OSNR

## [0.2.17] - 2021-10-29

### Fixed

- Tx Polarization Dependent Power: VOA unit fixed

## [0.2.16] - 2021-10-29

### Fixed

- Fixed Neo USB devices connection issue

## [0.2.15] - 2021-10-29

### Changed

- Optimise osa operation in test cases:
  - Tx In-Band OSNR
  - Tx Out-of-Band OSNR

## [0.2.14] - 2021-10-28

### Changed

- Update pyinst library, which has built in dll dependencies of NeoSW.

## [0.2.13] - 2021-10-25

### Fixed

- Key error of test cases related to 'POLC2 Rotation Mode'

## [0.2.12] - 2021-10-25

### Changed

- Compliance support of cmis revision <= 4.0

## [0.2.11] - 2021-10-25

### Fixed

- Fixed sqlite.dll issue: replace to support json field

## [0.2.10] - 2021-10-22

- Add new parameter for test-suite: EVT Test
  - POLC2 Rotation Mode, options: Tornado (fixed axis) / Tornado (rotating axis)

## [0.2.9] - 2021-09-08

### Fixed

- Remove all listeners of rpcServer before kill it, or there is a chance of Error alerted when close app.

## [0.2.8] - 2021-09-08

### Fixed

- RPC timeout when exporting to JMP on slow computers.
- SiUSBXp.dll is included in the installation.
- Chart display error (caused by version compliance issue between vue-chartjs and Chart.js)

### New

- Option to show in folder after generating report or exporting to JMP.

## [0.2.7] - 2021-09-07

### Fixed

- Issue when export for JMP when primary key is not defined.

## [0.2.6-beta] - 2021-09-02

### Fixed

- Fixed OPC timeout error when set oma result length too long.

## [0.2.5] - 2021-08-31

### Changed

- Test Case: Tx Polarization Dependent Power: Set Tx VOA to 35mA instead of mute DSP lane output.
- OMA setting: Set compensate CD/PMD true before test started. Set Custom IQ Demod Result Length to 2000 after frequency change. 
- Test Case: Laser Center Frequency Accuracy: mute X VOA instead.
- Test Case: DGD Monitor Accuracy: configurate DGD points in config file.
- Data Processor: Scattar3D: fix if no primary key is defined.

## [0.2.4] - 2021-07-14

### Added

- Test case for both 'EVT Test' and 'EVT Test Lite':
  - Test Case: Additional Monitor Data Collection
  - New config field to support this test case:
    - Addt Mon Data: OSNR Points
    - Addt Mon Data: Rx Pow Points

## [0.2.3] - 2021-07-01

### Fixed

- Issue RPC server crashed after long time run, caused by max buffer exceeded of child process.

## [0.2.2] - 2021-06-30

### Changed

- Enable asar while app build, exclude ElectronPythonSubProcess
- Optimise auto-update logic and UI
- App single instance lock

## [0.2.1] - 2021-06-30

### Changed

- PRBS Generator & Checker will not enable if PostFec Source is set to PCS in test suite 'EVT Test' and 'EVT Test Lite'

## [0.2.0] - 2021-06-29

### Changed

- Update to new GUI architecture with multiple optimizations

### Added

- App auto update

### Fixed

- Fixed compliance issues by using concurrent instead of gevent

## [0.1.36] - 2021-06-22

### Changed

- Set "RX_TIA_SD" Dpin to Low before test

## [0.1.35] - 2021-06-16

## Fixed

- Unit of X axis in "CFO Monitor Accuracy"

## [0.1.34] - 2021-06-07

### Fixed

- Crash issue of test case: 'OSNR Monitor Accuracy'
- Unit scale of VDM:
  - DGD
  - PDL
  - EVM

## [0.1.33] - 2021-05-27

### Fixed

- Issue of test suite 'EVT Test Lite' when using PCS for post-FEC

## [0.1.32-Update1] - 2021-05-26

### Fixed

- Fix that param "This Temperature Source Sucks" is not added to param list.

## [0.1.32] - 2021-05-26

### Added

- Add param "This Temperature Source Sucks" to test configuration file of test-suites "EVT Test" and "EVT Test Lite", in case that one of our ATS is not stable (variation no less than 0.6°C). If enabled, the variation limit of the temperature source will be relaxed to 1°C. Never enable it when the temperature source is normal.

## [0.1.31] - 2021-05-25

### Fixed

- Set bank explicitly when getting VDM values
- Fix issue when teardown reference module if Block "DUT/Ref-Module Teardown" is enabled.

## [0.1.30] - 2021-05-20

### Changed

- When DUT/Ref-Module post-fec source set to PCS:
  - Enable PCS Egress Generator
  - Disable PCS Ingress Generator
  - Disable PCS Egress Checker
  - Enable PCS Ingress Checker

## [0.1.29] - 2021-05-20

### Fixed

- Call init_vdm_mapping while trx initializing.

## [0.1.28] - 2021-05-19

### Changed

- Updated trx_cmis lib to support new dynamic vdm realization, which is compliant with CMIS
  
### Added

- Added test case: "OSNR Monitor Accuracy". A new config key is added to test configuration file: "OSNR Monitor Points"

## [0.1.27] - 2021-05-10

### Changed

- "CFO Monitor Accuracy": restart data-path before get CFO monitor

## [0.1.26] - 2021-05-10

### Changed

- Change "Block DUT Teardown" to "Block DUT/Ref-Module Teardown", both DUT and Ref-Module will keep status after test

## [0.1.25] - 2021-05-07

### Fixed

- CD Monitor Accuracy: Fix polarization
- CFO Monitor Accuracy: Fix polarization, add 30s delay in case module ABC need time to adjust
- Use PCS Egress instead of Ingress when set Post-FEC source to PCS
- Set Post-FEC source after module reset after setting voltage.

## [0.1.24] - 2021-03-05

### Fixed

- Fixed Pre-FEC BER at OSNR tolerance

## [0.1.23] - 2021-03-02

### Fixed

- Fix Test Case: \[RefTx] CD Tolerance

## [0.1.22] - 2021-03-01

### Changed

- Update Export to JMP® function

## [0.1.21] - 2021-02-26

### Fixed

- Issues in several test cases.

## [0.1.20] - 2021-02-25

### Added

- Add new test cases:
  - PMD Tolerance
  - PDL Tolerance
  - SOP Tolerance
  - \[RefTx] PMD Tolerance
  - \[RefTx] PDL Tolerance
  - \[RefTx] SOP Tolerance

## [0.1.19] - 2021-02-25

### Added

- Add a new button on Test Data panel: Export for JMP®, to export generated data suitable for JMP to process

## [0.1.18] - 2021-02-23

### Added

- Add new instrument slot for test suite "EVT Test": CD-OPM1, CD-VOA1, CD-OPM2, CD-VOA2, CD-OPM3, CD-VOA3, each pair of OPM & VOA is optional. If both VOA and OPM in a pair are available, the monitor value of OPM will be adjusted to -0.5 dBm. This is to adjust the optical power into each long-distance fiber.

## [0.1.17] - 2021-02-06

### Fixed
- Test Case CFO Tolerance, removed requirement of wavemeter.
- Optical Path of test case: EVM Monitor Accuracy

## [0.1.16] - 2021-02-05

### Fixed
- OMA related test skipped if VOA2 is empty

## [0.1.15] - 2021-02-04

### Added
- Add support for PSY-101
- Add a param in TSConf for both EVT and EVT Lite test suite: Post-FEC Source

### Changed
- Support new feature in framework level: if an instrument frequency does not support, only test cases that relies on the instrument will be skipped.
- Check devices presentation before test case, if a device required does not exist, the test case will be skipped.

## [0.1.14] - 2021-02-02

### Added
- Update trx-cmis, support adc/dac operations
- Add option in test configuration file, enable/disable module reset after Vcc changed.

### Changed
- New Icon

### Fixed
- Fix: Total Output Power with Tx Disabled, add 1s delay after enter DataPathActivated
- Fix some other issues in test cases

## [0.1.13] - 2021-01-19

### Added
- New page in settings: *Settings/Help/About*
- Add Test Cases:
  - \[RefTx] Rx OSNR Tolerance
  - \[RefTx] Rx Sensitivity

### Changed
- Sequence of test cases in EVT Test

## [0.1.12] - 2021-01-15

###  Added
- New page in settings: *Settings/Help/Changelog*
- App start-up page

## [0.1.11] - 2021-01-14

### Added
- New page in settings: *Settings/Help/Debug* to read and export logs.

### Fixed
- Issue in test case: *DGD Monitoring Accuracy*.


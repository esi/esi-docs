# Fitting Formats

There are several formats for representing fittings:

## EFT

EFT stands for "EVE Fitting Tool", which used to be a popular third-party application for ship fitting.
Although the application is long gone, the format it used has since been adopted by many tools and the game itself.
This is the format used when the "Copy to Clipboard" action is used in the in-game fitting window, and the format expected for the "Import from Clipboard" action.

### Format

1. First line lists the hull and fitting name, in square brackets, separated by a comma
2. Low slot modules
3. Medium slot modules and charge (if available)
4. High slot modules and charge (if available) (i.e., 125mm Railgun I, Antimatter Charge S)
5. Rigs
6. Subsystems
7. Services (for structure fits)
8. Drones / fighters in drone / fighter bay with amount (i.e., Warrior II x2)
9. Items in cargo bay with amount (i.e., Antimatter Charge M x42)

Sections 2–7 are separated by an empty line, sections 7–9 are separated by two empty lines.

Drones and items in cargo can have counts indicated with a ` x42` suffix for 42 units, for example.

Modules can have the suffix `/offline` to indicate they are offline. However, although in-game imports these fits, the `/offline` suffix is ignored. The module will still be imported as online.

Empty slots are indicated by `[Empty <name> slot]` where `<name>` is one of `low`, `med`, `high`, `rig`, `service`, however this is not present when exporting from the game, but still considered valid when importing.

Type names can be specified in any localized format, not only English.

### Example

```
[Heron Navy Issue, Deepflow Rift Dredger]
Inertial Stabilizers II
Inertial Stabilizers II /offline

Scan Pinpointing Array II
Scan Rangefinding Array II
Scan Acquisition Array II
Compact EM Shield Amplifier
Compact Thermal Shield Amplifier

Small Tractor Beam II
Small Tractor Beam II
Core Probe Launcher II
Improved Cloaking Device II

Small Gravity Capacitor Upgrade II
Small Core Defense Field Extender I




Sisters Core Scanner Probe x8
```

## DNA

Ship DNA is a compact format describing a fit in a single line.
This is the format used when linking fits in chat in-game.

### Format

The formal grammar is as follows:

```
DNA -> SHIP ':' HIGHS ':' MEDS ':' LOWS ':' RIGS ':' CHARGES
SHIP -> SHIP_TYPE_ID ( ':' SUBSYSTEM_ID ':' SUBSYSTEM_ID ':' SUBSYSTEM_ID ':' SUBSYSTEM_ID ':' SUBSYSTEM_ID )
HIGHS -> EMPTY | MODULE ( ':' MODULE )
MEDS -> EMPTY | MODULE ( ':' MODULE )
LOWS -> EMPTY | MODULE ( ':' MODULE )
RIGS -> EMPTY | MODULE ( ':' MODULE )
CHARGES -> EMPTY | CHARGE ( ':' CHARGE )
MODULE -> MODULE_ID ( '_' ) ';' QUANTITY
CHARGE -> CHARGE_ID ';' QUANTITY
SHIP_TYPE_ID -> the typeID of a ship
SUBSYSTEM_ID -> the typeID of the fitted subsystems
MODULE_ID -> the typeID of the fitted module
CHARGE_ID -> the typeID of a charge or a drone
QUANTITY -> an integer quantity of the type
```

Module IDs can be followed by an underscore to indicate they are unfitted. Charges are always considered unfitted.

### Example

`72904:4250;2:4258;1:11577;1:33199;1:33201;1:33197;1:9580;1:9568;1:1405;2:31220;1:31788;1:30488;8::`

As a chat link:
`<url=fitting:72904:4250;2:4258;1:11577;1:33199;1:33201;1:33197;1:9580;1:9568;1:1405;2:31220;1:31788;1:30488;8::>Deepflow Rift Dredger</url>`

## XML

This is the format used when exporting fits to a file in-game, or importing from a file. The format supports multiple fits in a single data structure.

### Example

```xml
<?xml version="1.0" ?>
<fittings>
    <fitting name="Deepflow Rift Dredger">
        <description value=""/>
        <shipType value="Heron Navy Issue"/>
        <hardware slot="low slot 0" type="Inertial Stabilizers II"/>
        <hardware slot="low slot 1" type="Inertial Stabilizers II"/>
        <hardware slot="hi slot 0" type="Small Tractor Beam II"/>
        <hardware slot="hi slot 1" type="Small Tractor Beam II"/>
        <hardware slot="hi slot 2" type="Core Probe Launcher II"/>
        <hardware slot="med slot 4" type="Compact Thermal Shield Amplifier"/>
        <hardware slot="med slot 3" type="Compact EM Shield Amplifier"/>
        <hardware slot="hi slot 3" type="Improved Cloaking Device II"/>
        <hardware qty="8" slot="cargo" type="Sisters Core Scanner Probe"/>
        <hardware slot="rig slot 0" type="Small Gravity Capacitor Upgrade II"/>
        <hardware slot="rig slot 1" type="Small Core Defense Field Extender I"/>
        <hardware slot="med slot 2" type="Scan Acquisition Array II"/>
        <hardware slot="med slot 0" type="Scan Pinpointing Array II"/>
        <hardware slot="med slot 1" type="Scan Rangefinding Array II"/>
    </fitting>
</fittings>
```

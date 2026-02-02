# System Security

You can find the security status of any solar system in [SDE](../services/static-data/index.md)'s `mapSolarSystems.jsonl` file.
It is under the `securityStatus` field, which is a floating point value given with full precision, usually 6 decimal places.

Not to be confused with the `securityClass` field, which is a string value with unknown meaning.

In-game, the security status (also known as security level) is shown with 1 decimal place precision, from -1.0 to 1.0. In the SDE, it is given with full precision and needs to be rounded to 1 decimal place to match the in-game display.

## Rounding

Security status rounding follows normal rounding rules, with one exception:
if the security status is in the range $0.0 < x < 0.05$, it is rounded to 0.1, instead of 0.0. In other words, if the security status is positive, however slightly, the rounded result will always be at least 0.1.

<h3>Example</h3>

--8<-- "snippets/formulae/security-status-rounding.md"

## Security Class

Various game mechanics rely on the security class of a system, which can be one of the following:

- High Security (high-sec), where the security status is $x ≥ 0.45$, or the rounded security status is $x ≥ 0.5$
- Low Security (low-sec), where the security status is $0.0 < x < 0.45$, or the rounded security status is $0.1 ≤ x ≤ 0.4$
- Null Security (null-sec), where the security status is $x ≤ 0.0$, or the rounded security status is $x ≤ 0.0$

<h3>Example</h3>

--8<-- "snippets/formulae/security-class.md"

## Security Status Colors

In-game, the security status is often colored according to the following table:

| Color                                                | Color hex code | Security status |
|------------------------------------------------------|----------------|-----------------|
| <div style="height:20px; background:#2C75E1;"></div> | #2C75E1        | ≥ 1.0           |
| <div style="height:20px; background:#399AEB;"></div> | #399AEB        | ≥ 0.9           |
| <div style="height:20px; background:#4ECEF8;"></div> | #4ECEF8        | ≥ 0.8           |
| <div style="height:20px; background:#60DBA3;"></div> | #60DBA3        | ≥ 0.7           |
| <div style="height:20px; background:#71E754;"></div> | #71E754        | ≥ 0.6           |
| <div style="height:20px; background:#F5FF83;"></div> | #F5FF83        | ≥ 0.5           |
| <div style="height:20px; background:#DC6C06;"></div> | #DC6C06        | ≥ 0.4           |
| <div style="height:20px; background:#CE440F;"></div> | #CE440F        | ≥ 0.3           |
| <div style="height:20px; background:#BB1116;"></div> | #BB1116        | ≥ 0.2           |
| <div style="height:20px; background:#731F1F;"></div> | #731F1F        | ≥ 0.1           |
| <div style="height:20px; background:#8D3163;"></div> | #8D3163        | else            |

# Useful Formulae

## Ordinary Objects
An ordinary object is any object that does not fall withing any of the other categories described below.

Let the 3D vectors $p_d$ and $p_s$ represent the object’s position and the warp’s origin, respectively; and $\vec{v}$ the directional vector from $p_s$ to $p_d$. Let $r$ be the object’s radius.

The object’s warp-in point is the vector $p_s + \vec{v} - r\hat{v}$.

## Large Objects
A large object is any celestial body whose radius exceeds 90 kilometres (180 kilometres in diameter), except planets.

Let $x$, $y$, and $z$ represent the object’s coordinates. Let $r$ be the object’s radius.

The object’s warp-in point is the vector $\left(x + (r + 5000000)\cos{r} \\, y + 1.3r - 7500 \\, z - (r + 5000000)\sin{r} \\ \right).$

## Planets

The warp-in point of a planet is determined by the planet's ID, its location, and radius.

Let $x$, $y$, and $z$ represent the planet's coordinates. Let $r$ be the planet's radius.

The planet's warp-in point is the vector $\left(x + d \sin{\theta}, y + \frac{1}{2} r \sin{j}, z - d \cos{\theta}\right)$
where:

$$
d = r(s + 1) + 1000000
$$

$$
\theta = \sin^{-1}\left(\frac{x}{|x|} \cdot \frac{z}{\sqrt{x^2 + z^2}}\right) + j
$$

$$
s|_{0.5 \leq s \leq 10.5} = 20\left(\frac{1}{40}\left(10\log_{10}\left(\frac{r}{10^6}\right) - 39\right)\right)^{20} + \frac{1}{2}
$$

Now, $j$ is a special snowflake. Its value is the Python equivalent of `(random.Random(planetID).random() - 1.0) / 3.0`.

<h3>Example</h3>

--8<-- "snippets/formulae/warp-in.md"

## Skillpoints needed per level

The skillpoints needed for a level depend on the skill rank.

$y_{skillpoints} = 2^{2.5(x_{skilllevel}-1)} \cdot 250 \cdot r_{skillrank}$

<h3>Skillpoints for common ranks</h3>

| Rank   | Level 1 | Level 2 | Level 3 | Level 4 | Level 5   |
|--------|---------|---------|---------|---------|-----------|
| **1**  | 250     | 1.414   | 8000    | 45,254  | 256,000   |
| **2**  | 500     | 2,828   | 16,000  | 90,509  | 512,000   |
| **3**  | 750     | 4,242   | 24,000  | 135,764 | 768,000   |
| **4**  | 1000    | 5,656   | 32,000  | 181,019 | 1,024,000 |
| **5**  | 1250    | 7,071   | 40,000  | 226,274 | 1,280,000 |
| **6**  | 1500    | 8,485   | 48,000  | 271,529 | 1,536,000 |
| **7**  | 1750    | 9,899   | 56,000  | 316,784 | 1,792,000 |
| **8**  | 2000    | 11,313  | 64,000  | 362,039 | 2,048,000 |
| **9**  | 2250    | 12,727  | 72,000  | 407,293 | 2,304,000 |
| **10** | 2500    | 14,142  | 80,000  | 452,548 | 2,560,000 |
| **11** | 2750    | 15,556  | 88,000  | 497,803 | 2,816,000 |
| **12** | 3000    | 16,970  | 96,000  | 543,058 | 3,072,000 |
| **13** | 3250    | 18,384  | 104,000 | 588,312 | 3,328,000 |
| **14** | 3500    | 19,798  | 112,000 | 633,567 | 3,584,000 |
| **15** | 3750    | 21,213  | 120,000 | 678,822 | 3,840,000 |
| **16** | 4000    | 22,627  | 128,000 | 724,077 | 4,096,000 |

## Skillpoints per minute


The skillpoints generated each minute depend on the primary $(a_{primary})$ and secondary attribute $(a_{secondary})$ of the skill.

$$
y_{skillpointsPerMinute} = a_{primary} + {a_{secondary} \over 2}
$$

## Target lock time

The target lock time ($t_{targetlock}$) in seconds depends on the ship's scan resolution ($s$) and the target's signature radius ($r$)

$$
t_{targetlock} = {40000 \over s \cdot asinh(r)^2}
$$

## Alignment time

The ship alignment time ($t_{align}$) depends on the ship's inertia modifier ($i$) and the ships mass ($m$)

$$
t_{align} = { ln(2) \cdot i \cdot m \over 500000 }
$$
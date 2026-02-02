enum class SecurityClass {
    HighSec, LowSec, NullSec
}

fun Double.getSecurityClass() = when {
    this >= 0.45 -> SecurityClass.HighSec
    this > 0.0 -> SecurityClass.LowSec
    else -> SecurityClass.NullSec
}

import kotlin.math.roundToInt

fun Double.roundSecurity() = when {
    this == 0.0 -> 0.0
    this in 0.0..0.05 -> (this * 10 + 0.5).roundToInt() / 10.0
    else -> (this * 10).roundToInt() / 10.0
}

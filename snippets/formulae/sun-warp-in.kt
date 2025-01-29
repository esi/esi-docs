import kotlin.math.*

fun getSunWarpInPoint(radius: Double): Triple<Double, Double, Double> {
    val x = (radius + 100000) * cos(radius)
    val y = 0.2 * radius
    val z = -(radius + 100000) * sin(radius)
    return Triple(x, y, z)
}

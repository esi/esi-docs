import kotlin.math.*

fun getLargeObjectWarpInPoint(x: Double, y: Double, z: Double, radius: Double): Triple<Double, Double, Double> {
    val x = (radius + 5000000) * cos(radius)
    val y = 1.3 * radius - 7500
    val z = -(radius + 5000000) * sin(radius)
    return Triple(x, y, z)
}

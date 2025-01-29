import org.apache.commons.math3.random.MersenneTwister
import kotlin.math.*

fun getPlanetWarpInPoint(planetId: Int, x: Double, y: Double, z: Double, radius: Double): Triple<Double, Double, Double> {
    val j = (MersenneTwister(intArrayOf(planetId)).nextDouble() - 1) / 3
    val theta = asin((x / abs(x)) * (z / (sqrt(x.pow(2) + z.pow(2))))) + j
    val s = (20 * ((10 * log10(radius / 1000000) - 39) / 40).pow(20) + 0.5).coerceIn(0.5, 10.5)
    val d = radius * (s + 1) + 1000000
    return Triple(x + sin(theta) * d, y + radius * sin(j) / 2, z - cos(theta) * d)
}

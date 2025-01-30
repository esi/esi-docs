import java.time.Duration
import kotlin.math.*

private const val SEC = 10000000L

/**
 * @param baseValue This is the "qty_per_cycle" value as returned by ESI
 * @param cycleDuration Cycle duration, e.g. 2 hours
 * @param length The number of cycles in this extraction
 */
fun calculateExtractorValues(baseValue: Int, cycleDuration: Duration, length: Int): List<Long> {
    return buildList {
        val startTime = 0L
        val cycleTime = cycleDuration.toSeconds() * SEC
        for (i in 0 until length) {
            val currentTime = (i + 1) * cycleTime
            add(calculateExtractorValue(baseValue, startTime, currentTime, cycleTime))
        }
    }
}

private fun calculateExtractorValue(baseValue: Int, startTime: Long, currentTime: Long, cycleTime: Long): Long {
    val decayFactor = 0.012
    val noiseFactor = 0.8
    val cycleNum = max((currentTime - startTime + SEC) / cycleTime - 1, 0)
    val barWidth = cycleTime / SEC / 900.0
    val t = (cycleNum + 0.5) * barWidth
    val decayValue = baseValue / (1 + t * decayFactor)
    val phaseShift = baseValue.toDouble().pow(0.7)
    val sinA = cos(phaseShift + t * (1.0 / 12.0))
    val sinB = cos(phaseShift / 2.0 + t * (1.0 / 5.0))
    val sinC = cos(t * (1.0 / 2.0))
    val sinStuff = max(0.0, (sinA + sinB + sinC) / 3.0)
    val barHeight = decayValue * (1 + noiseFactor * sinStuff)

    val output = barWidth * barHeight
    // Round down, with integers also rounded down (123.0 -> 122)
    return if (output - output.toLong() == 0.0) output.toLong() - 1 else output.toLong()
}

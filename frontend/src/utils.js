export function progressMap(x, p, q) {
    /*
    x = current output length
    p = predicted output length
    q = progress at predicted output length
    */

    const a = 2 * (1 - q)

    const x_1 = x + p * (a - 1)

    const f_asymptote = (a * x_1) / (a * p + x_1)
    const f_linear = x_1 / p

    const f = (x_1 < 0 ? f_linear : f_asymptote) + 1 - a

    return f
}
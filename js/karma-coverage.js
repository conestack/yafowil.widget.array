const percentage = {
    lines: 26,
    statements: 26,
    functions: 28,
    branches: 6
}
var summary = require('./karma/coverage/coverage-summary.json');

for (let res in summary.total) {
    if (summary.total[res].pct < percentage[res]) {
        throw new Error(
        `Coverage too low on ${res},
        expected: ${percentage[res]},
        got: ${summary.total[res].pct}`
        );
    }
}

import { format, addMonths, isBefore, isAfter } from 'date-fns';

export const edate = (date: Date, months: number): Date => {
    return addMonths(date, months);
};

export const getInstalmentDate = (d2: Date): Date => {
    const dateRanges: [Date, Date][] = [
        [new Date(2026, 5, 15), new Date(2026, 9, 1)],
        [new Date(2026, 4, 15), new Date(2026, 8, 1)],
        [new Date(2026, 3, 15), new Date(2026, 7, 1)],
        [new Date(2026, 2, 15), new Date(2026, 6, 1)],
        [new Date(2026, 1, 15), new Date(2026, 5, 1)],
        [new Date(2026, 0, 15), new Date(2026, 4, 1)],
        [new Date(2025, 11, 15), new Date(2026, 3, 1)],
        [new Date(2025, 10, 15), new Date(2026, 2, 1)],
        [new Date(2025, 9, 15), new Date(2026, 1, 1)],
        [new Date(2025, 7, 15), new Date(2026, 0, 5)],
    ];

    for (const [cutoff, result] of dateRanges) {
        if (isAfter(d2, cutoff) || d2.getTime() === cutoff.getTime()) {
            return result;
        }
    }
    return new Date(2025, 10, 1);
};
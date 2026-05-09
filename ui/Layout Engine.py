from collections import defaultdict

class LayoutEngine:

    @staticmethod
    def group(buttons):

        rows = defaultdict(list)

        for b in buttons:
            rows[b["row"]].append(b)

        for r in rows:
            rows[r].sort(key=lambda x: x["col"])

        return rows
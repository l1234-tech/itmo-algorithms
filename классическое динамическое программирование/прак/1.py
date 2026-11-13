# Команда 3
class Solution:
    def rob(self, nums: List[int]) -> int:
        prev_for_2 = 0
        prev_for_1 = 0

        for x in nums:
            current = max(prev_for_1, prev_for_2 + x)

            prev_for_2 = prev_for_1
            prev_for_1 = current

        return prev_for_1
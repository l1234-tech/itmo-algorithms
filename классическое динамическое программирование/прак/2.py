class Solution:
    def minPathSum(self, grid: list[list[int]]) -> int:
      columns, rows = len(grid), len(grid[0])
      dp = [0] * rows
      for column in range(columns):
        for row in range(rows):
          if row == 0 and column == 0:  # лево-верх
            dp[0] = grid[0][0]
          elif row == 0:  # лево
            dp[0] += grid[column][0]
          elif column == 0:  # верх
            dp[row] = dp[row-1] + grid[0][row]
          else:
            dp[row] = min(dp[row], dp[row-1]) + grid[column][row]
        return dp[-1]

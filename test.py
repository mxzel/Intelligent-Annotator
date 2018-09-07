
def rotate(nums, k):
    """
    :type nums: List[int]
    :type k: int
    :rtype: void Do not return anything, modify nums in-place instead.
    """
    nums[0:(len(nums)-k)%len(nums)] = nums[0:(len(nums)-k)%len(nums)][::-1]
    nums[(len(nums)-k)%len(nums):len(nums)] = nums[(len(nums)-k)%len(nums):len(nums)][::-1]
    nums.reverse()
    return nums

test_data = [1,2,3,4,5,6,7 ]
k = 3
rotate(test_data, k)

Complexity Analysis
 The time complexity of this code is  O(N×M), where  N is the number of schools and M is the number of institutes. The space complexity is also O(N×M) due to storing the close schools. How to Improve Performance:
  Batch the Geolocation Requests: If the API supports batch requests, we can reduce the number of API calls by sending multiple addresses at once.
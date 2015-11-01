var app = angular.module('app', []);
app.factory('Request', function ($http) {
    var baseURL = "/";
    return {
        get: function (requestURL, data) {
            var arr = [];
            for (var count = 0; count < Object.keys(data).length; count++) {
                arr.push(Object.keys(data)[count] + "=" + data[Object.keys(data)[count]])
            }
            var promise = $http({
                method: 'GET',
                url: baseURL + requestURL + "?" + arr.join("&"),
                timeout: 30000
            })
            return promise;
        },
        post: function (requestURL, data) {
            var promise = $http({
                method: 'POST',
                url: baseURL + requestURL,
                data: {
                    'data': JSON.stringify(data)
                },
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            return promise;
        }
    }
})
.controller('SearchCtrl', function($scope, Request){
		$scope.search = {
			keyword: ""
		}
		$scope.results = [];
		$scope.palette = [];
		$scope.cluster = [];
		$scope.search.submit = function(){
			Request.get('search', {
				q: $scope.search.keyword,
				limit: 20
			}).then(function(response){
				var data = response.data;
				console.log(data);
				$scope.results = data.results;
				$scope.palette = data.palette;
				$scope.cluster = data.cluster.sort(function(a, b){return a.count < b.count});
			})
		}
})
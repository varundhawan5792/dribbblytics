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
		$loading = false;
		$scope.search = {
			keyword: ""
		}
		$scope.results = [];
		$scope.palette = [];
		$scope.cluster = [];
		$scope.search.submit = function(){
			$scope.loading = true;
			Request.get('search', {
				q: $scope.search.keyword,
				limit: 24
			}).then(function(response){
				var data = response.data;
				console.log(data);
				$scope.loading = false;
				$scope.results = data.results;
                $scope.images = data.images;
				$scope.palette = data.palette;
				var totalColors = $scope.palette.length;
				$scope.cluster = data.cluster
									 .sort(function(a, b){return a.count < b.count})
									 .map(function(a){
									 	var percentage = (a.count / totalColors) * 100
									 	a.percentage = Math.round( percentage * 10 ) / 10;
									 	return a;
									 });

			})
		}
})

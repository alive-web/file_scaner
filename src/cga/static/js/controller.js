maineControllers = angular.module('maineControllers', []);

maineControllers.controller('fileController', function ($scope, $http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    $scope.get_all_versions = function(){
        $scope.tog = this.file.path_name
        $http.post('http://127.0.0.1:8000/api/files/', {"id": this.file.id}).success(function(data) {
        $scope.versions = data;
    });
    };
    $http.post('http://127.0.0.1:8000/api/files/').success(function(data) {
        $scope.files = data;
    });
});

maineControllers.controller('logController', function ($scope, $http, $cookies, $filter) {
    var date = new Date();
    $scope.date_event_to = new Date($filter("date")(date, 'yyyy, MM, dd'))
    $scope.date_event_from = new Date($filter("date")(date.setDate(date.getDate() - 1), 'yyyy, MM, dd'))
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    $scope.get_events = function(){
        $http.post('http://127.0.0.1:8000/api/logs/', {'from':$scope.date_event_from,
            'to':$scope.date_event_to}).success(function(data){$scope.files = data;});
    };
    $scope.get_events()
});
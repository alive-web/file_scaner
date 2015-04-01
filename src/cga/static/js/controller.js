var app = angular.module("app", ["ui.router", 'ngCookies']);

app.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise("/files");

    $stateProvider
        .state('maine', {
            url: "/",
            templateUrl: "static/templates/index.html"
        })
        .state('maine.file_system', {
            url: "files",
            templateUrl: "static/templates/files.html",
            controller: "fileController"
        })
        .state('maine.logs', {
            url: "logs",
            templateUrl: "static/templates/logs.html",
            controller: "logController"
        });
}]);

app.controller('fileController', function ($scope, $http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    $http.post('http://127.0.0.1:8000/get_files/').success(function(data) {
        $scope.files = data;
    });
});

app.controller('logController', function ($scope, $http, $cookies) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    console.log($scope.event)
    $scope.get_events = function(){
        console.log($scope.event.to)
        $http.post('http://127.0.0.1:8000/api_logs/', {'from':"5",
            'to':"65"}).success(function(data){
        $scope.files = data;
    });
    };
    $http.post('http://127.0.0.1:8000/api_logs/').success(function(data) {
        $scope.files = data;
    });
});
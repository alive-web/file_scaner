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
        //.state('maine.file_system.versions', {
        //    url: "/versions/:path",
        //    templateUrl: "static/templates/versions.html",
        //    controller: "versionController"
        //});
}]);

app.controller('fileController', function ($scope, $http, $cookies) {
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

app.controller('logController', function ($scope, $http, $cookies, $filter) {
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

//app.controller('versionController', function ($scope) {
//    console.log($scope)
//});
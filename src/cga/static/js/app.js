var app = angular.module("app", [
    "ui.router",
    "ngCookies",
    "maineControllers"
]);

app.config(['$stateProvider', '$urlRouterProvider',  function ($stateProvider, $urlRouterProvider) {
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


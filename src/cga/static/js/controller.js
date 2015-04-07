maineControllers = angular.module('maineControllers', []);

maineControllers.controller('fileController', function ($scope, $http, $cookies, $compile) {
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
    $scope.get_all_versions = function(){
        $scope.tog = this.file.path_name
        $http.post('http://127.0.0.1:8000/api/files/', {"id": this.file.id}).success(function(data) {
        $scope.versions = data;
        });
    };
    $scope.add = function(file){
        if (file.child.length){
            file.child=[];
        }
        else{
            var j = 0;
            $scope.check = true;
            for (var i in $scope.all_files){
                if ($scope.all_files[i].parent == file.path_name){
                    file.child.push($scope.all_files[i]);
                    file.child[j].child = [];
                    j++;
                }
            }
        }
    };
    $http.post('http://127.0.0.1:8000/api/files/').success(function(data) {
        $scope.all_files = data;
        var j = 0;
        $scope.tree = [];
        for (var i in data){
            if (data[i].parent == "None"){
                $scope.tree.push(data[i]);
                $scope.tree[j].child = [];
                j++;
            };
        };

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

maineControllers.directive("tree", function($compile){
    return {
		templateUrl: "static/templates/get_files_in_dir.html",
		restrict: 'A',
        //link: function (scope, elm) {
        //    scope.add = function($scope){
        //        console.log(this.file.path_name);
        //        console.log($scope)
        //        elm.after($compile("<div class='col-md-2' tree></div>")(scope));
        //    }
        //}
	};
});
'use strict';

angular.module('hangout', [
    'ngRoute',
    'ngCookies',
//    'angularFileUpload',
    'hangout.services',
    'hangout.controllers',
    ]).
    constant('urls', {'part': '/static/partials', 'api': '/api'}).
    config(['$interpolateProvider', function($interpolateProvider){
        $interpolateProvider.startSymbol('[[');
        $interpolateProvider.endSymbol(']]');
    }]).
    config(['$httpProvider', function($httpProvider){
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    }]).
    config(['$routeProvider', '$locationProvider', 'urls', function($routeProvider, $locationProvider, urls) {
        //Route configure
        $locationProvider.html5Mode(true);
        $locationProvider.hashPrefix = '';
        $routeProvider.when('/', {templateUrl: urls.part + '/homepage.html', controller: 'homepageCtrl', title: 'homepage', tag_name: 'homepage'});
	    $routeProvider.when('/login',{
            templateUrl: urls.part + '/login.html', 
            controller: 'loginCtrl', 
            controllerAs: 'vm',
            title: 'login', 
            tag_name: 'login'});
        $routeProvider.when('/register',{
            templateUrl: urls.part + '/register.html', 
            controller: 'registerCtrl', 
            controllerAs: 'vm',
            title: 'register', 
            tag_name: 'register'});
	    $routeProvider.otherwise({redirectTo: '/'});
    }]).
    run(['$location', '$rootScope', function($location, $rootScope){
        //Configure header title of the page
        $rootScope.$on('$routeChangeSuccess', function(event, current, previous){
            $rootScope.title = current.$$route.title;
            $rootScope.tag_name = current.$$route.tag_name;
        });
    }]);

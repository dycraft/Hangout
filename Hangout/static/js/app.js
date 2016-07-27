'use strict';

angular.module('hangout', [
    'ngRoute',
    'ngCookies',
//    'angularFileUpload',
    'hangout.services',
    'hangout.controllers',
    'hangout.directives',
    'angular-notification-icons',
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
        $routeProvider.when('/profile',{
            templateUrl: urls.part + '/profile.html', 
            controller: 'profileCtrl', 
            controllerAs: 'vm',
            title: 'profile', 
            tag_name: 'profile'});
        $routeProvider.when('/follow_info', {
            templateUrl: urls.part + '/follow_info.html',
            controller: 'followInfoCtrl',
            title: 'followInfo',
            tag_name: 'followInfo'});
        $routeProvider.when('/activity',{
            templateUrl: urls.part + '/activity.html', 
            controller: 'activityCtrl', 
            title: 'activity', 
            tag_name: 'activity'});
        $routeProvider.when('/act_info/:act_id',{
            templateUrl: urls.part + '/act_info.html', 
            controller: 'actInfoCtrl', 
            title: 'actInfo', 
            tag_name: 'actInfo'});
        $routeProvider.when('/user_info/:user_id',{
            templateUrl: urls.part + '/user_info.html', 
            controller: 'userInfoCtrl', 
            title: 'userInfo', 
            tag_name: 'userInfo'});
        $routeProvider.when('/tag_info/:tag_name',{
            templateUrl: urls.part + '/tag_info.html', 
            controller: 'tagInfoCtrl', 
            title: 'tagInfo', 
            tag_name: 'tagInfo'});
	    $routeProvider.otherwise({redirectTo: '/'});
    }]);

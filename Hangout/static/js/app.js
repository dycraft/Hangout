'use strict';

angular.module('hangout', []).
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
        $routeProvider.when('/', {templateUrl: urls.part + '/homepage.html', controller: 'HomepageCtrl', title: '首页', tag_name: 'homepage'});
	    $routeProvider.when('/test',{templateUrl: urls.part + '/test.html', controller: 'TestCtrl', title: 'test', tag_name: 'testpage'});
	    $routeProvider.when('/news/:news_id/detail', {templateUrl: urls.part + '/newspage.html', controller: 'NewspageCtrl', title: 'news', tag_name: 'newspage'});
	    $routeProvider.when('/act/:act_id/detail', {templateUrl: urls.part + '/actpage.html', controller: 'ActpageCtrl', title: 'act', tag_name: 'actpage'});
	    $routeProvider.when('/news/:news_list_id/list', {templateUrl: urls.part + '/newslist.html', controller: 'NewslistCtrl', title: 'newslist', tag_name: 'newslistpage'});
	    $routeProvider.when('/act/:act_list_id/list', {templateUrl: urls.part + '/actlist.html', controller: 'ActlistCtrl', title: 'actlist', tag_name: 'actlistpage'});
    	$routeProvider.when('/news/get_categories', {templateUrl: urls.part + '/newscates.html', controller: 'NewscateCtrl', title: 'newscate', tag_name: 'newscatepage'});
    	$routeProvider.when('/act/get_categories', {templateUrl: urls.part + '/actcates.html', controller: 'ActcateCtrl', title: 'actcate', tag_name: 'actcatepage'});
    	$routeProvider.when('/news/:key/search', {templateUrl: urls.part + '/searchres.html', controller: 'NewsSearchCtrl', title: 'newsSearch', tag_name: 'newsSearchpage'});
    	$routeProvider.when('/act/:key/search', {templateUrl: urls.part + '/act_searchres.html', controller: 'ActSearchCtrl', title: 'ActSearch', tag_name: 'actSearchpage'});
    	$routeProvider.when('/news', {templateUrl: urls.part + '/newsindex.html', controller: 'NewsIndexCtrl', title: 'newsIndex', tag_name:' newsIndexpage'});
        $routeProvider.otherwise({redirectTo: '/'});
    }]);

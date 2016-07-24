(function() {
  'use strict';

  angular.module('hangout.directives', [])
  	.directive('activity', function() {
    	return {
        restrict: 'E',
        link: function(scope, element, attrs) {
          scope.contentUrl = '/static/partials/' + attrs.ver + '.html';
          attrs.$observe("ver", function(v) {
          	scope.contentUrl = '/static/partials/' + v + '.html';
          });
        },
        template: '<div ng-include="contentUrl"></div>'
	    }	
  	});
})();
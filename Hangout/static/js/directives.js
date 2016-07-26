(function() {
  'use strict';

  angular.module('hangout.directives', [])
  	.directive('activity', function() {
    	return {
        restrict: 'E',
        link: function(scope, element, attrs) {
          scope.contentUrl = '/static/partials/' + attrs.ver + '.html';
          attrs.$observe("ver", function(v) {
          	scope.contentUrl = '/static/partials/' + v + '.html?10';
          });
        },
        template: '<div ng-include="contentUrl"></div>'
	    }
  	})
    .directive('onFinishRenderFilters', function ($timeout, $parse) {
        return {
            restrict: 'A',
            link: function (scope, elem, attrs) {
                if (scope.$last === true) {
                    $timeout(function () {
                        scope.$emit('ngRepeatFinished');
                        if (!!attrs.onFinishRender) {
                            $parse(attr.onFinishRender)(scope);
                        }
                    });
                }
            }
        };
    });
})();

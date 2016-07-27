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
    })
    .directive('backToTop', function(){
      return {
        restrict: 'E',
        replace: true,
        template: '<div class="back-to-top"><i class="fa fa-chevron-up"></i></div>',
        link: function($scope, element, attrs) {
          $(window).scroll(function(){
            if ($(window).scrollTop() <= 0) {
              $(element).fadeOut();
            }
            else {
              $(element).fadeIn();
            }
          });
          $(element).on('click', function(){
            $('html, body').animate({ scrollTop: 0 }, 'fast');
          });
        }
      };
    });
})();

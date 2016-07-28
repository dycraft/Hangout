(function() {
  'use strict';

  angular.module('hangout.directives', [])
  	.directive('activity', function() {
    	return {
        restrict: 'E',
        link: function(scope, element, attrs) {
          scope.contentUrl = '/static/partials/' + attrs.ver + '.html';
          attrs.$observe("ver", function(v) {
          	scope.contentUrl = '/static/partials/' + v + '.html?6391';
          });
        },
        template: '<div ng-include="contentUrl"></div>'
	    };
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
        template: '<div class="back-to-top"><i class="fa fa-arrow-up"></i></div>',
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
    })
    .filter('subString', function() {
      return function(str, start, end) {
          if (str !== undefined) {
              return str.substr(start, end);
          }
      };
    })
    .directive('showMore', function() {
        return {
            restrict: 'AE',
            replace: true,
            scope: {
                text: '=',
                limit:'='
            },

            template: '<div><p ng-show="largeText"> {{ text | subString :0 :end }}.... <a href="javascript:;" ng-click="showMore()" ng-show="isShowMore">更多</a><a href="javascript:;" ng-click="showLess()" ng-hide="isShowMore">收起 </a></p><p ng-hide="largeText">{{ text }}</p></div> ',

            link: function(scope, iElement, iAttrs) {
                scope.end = scope.limit;
                scope.isShowMore = true;
                scope.largeText = true;
                console.log(123);
                if (scope.text.length <= scope.limit) {
                    scope.largeText = false;
                }

                scope.showMore = function() {

                    scope.end = scope.text.length;
                    scope.isShowMore = false;
                };

                scope.showLess = function() {

                    scope.end = scope.limit;
                    scope.isShowMore = true;
                };
            }
        };
    });

})();

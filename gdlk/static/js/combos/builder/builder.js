(function(window, angular) {
  'use strict';

  var builder = angular.module('gdlk.combos.builder', ['gdlk.utils']);

  builder.directive('builder', function() {
    return {
      restrict: 'E',
      scope: {
        commands: '=commands'
      },
      template: '<div class="preview"><command ng-repeat="cmd in commands" type="{{cmd.type}}" move="{{cmd.move}}"></command></div>'
    };
  });

})(window, window.angular);

(function(window, angular) {
  'use strict';

  var builder = angular.module('gdlk.combos.builder');

  builder.factory('typeOrder', function() {
    return [{
      key: 'stick',
      label: 'Stick'
    }, {
      key: 'sf4',
      label: 'Street Fighter IV'
    }, {
      key: 'mvc3',
      label: 'Marvel vs. Capcom 3',
    }, {
      key: 'separators',
      label: 'Separators'
    }];
  });

})(window, window.angular);

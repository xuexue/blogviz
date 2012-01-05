// Author : Jeeyoung Kim
// Utility code, formatted under its own function
// space.
(function($){
  /** Load a given tempplate, using the selector. */
  $.fn.compile = function() {
    var txt = this.contents()[0].data;
    var tmpl = _.template(txt);
    return tmpl;
  }

  /** Assertions */
  var AssertException = function(message) { this.message = message; }
  AssertException.prototype.toString = function () {
    return 'AssertException: ' + this.message;
  };

  var assert = function(exp, message) {
    if (!exp) {
      console.log("Assertion failed", message);
      throw new AssertException(message);
    }
  };
})(jQuery);

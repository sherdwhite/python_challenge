# This is an example of a custom filter that can be put into a template tag on a page to perform a custom function
from django import template

register = template.Library()  #Decorators are better

@register.filter(name='cut')  # This is a decorator which is a cleaner way of declaring this custom filter
def cut(value, arg):
    """
    This cuts out all the values of "arg" from a string!
    Example usage in HTML: <h1>{{ text|cut: 'hello' }}</h1>
    Result: would cut any instance of hello out of passed text.
    """
    return value.replace(arg,'')

#register.filter('cut',cut) #using decorators instead


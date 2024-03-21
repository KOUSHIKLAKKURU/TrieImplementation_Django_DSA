from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Word
from .trie import Trie

trie_instance = Trie()

def delete_word(request, word_id):
    try:
        word = Word.objects.get(pk=word_id)
        word.delete()
        return redirect('view_words')  # Redirect to the view_words page after deletion
    except Word.DoesNotExist:
        # Handle the case where the word does not exist
        return render(request, 'word_not_found.html')

def delete_words(request):
    words = Word.objects.all().order_by('word_text')
    context = {'words': words}
    return render(request, 'delete_word.html', context)
def view_words(request):
    words = Word.objects.all().order_by('word_text')
    context = {'words': words}
    return render(request, 'view_words.html', context)

def trie(request):
    return render(request,'trie_input.html')

def has_numbers_or_special_characters(word):
    # Check if the word contains numbers or special characters
    return any(char.isdigit() or not char.isalnum() for char in word)

def add_word(request):
    # Initialize messages to None
    error_message, warning_message, success_message = None, None, None

    if request.method == 'POST':
        word = request.POST.get('word')

        # Check if 'word' is not None before proceeding
        if word is None:
            error_message = "Invalid request. Please provide a valid word."
        else:
            # Check if the word contains numbers or special characters
            if has_numbers_or_special_characters(word):
                error_message = "Word should not contain numbers or special characters."
            else:
                # Check if the word is already present in the Trie
                if trie_instance.search(word):
                    warning_message = "Word already exists."
                else:
                    # Check if there are multiple words in the input
                    if ' ' in word:
                        error_message = "Multiple words cannot be added at once."
                    else:
                        # Insert the word into the Trie and database
                        trie_instance.insert(word)
                        Word.objects.create(word_text=word)
                        success_message = "Word added successfully."

                        # Redirect to the same view to prevent form resubmission
                        #return redirect(reverse('add_word'))

    # Pass messages to the template context
    data = {
        'error': error_message,
        'warning': warning_message,
        'success': success_message,
    }

    return render(request, 'add_word.html', data)

def get_suggestions(request):
    global trie_instance

    if request.method == 'GET':
        input_text = request.GET.get('input', '')

        if input_text:
            suggestions = trie_instance.search_prefix(input_text)
        else:
            suggestions = []

        return JsonResponse({'suggestions': suggestions})
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
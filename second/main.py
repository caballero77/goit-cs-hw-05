from concurrent.futures import ThreadPoolExecutor
import string
import requests
from collections import Counter, defaultdict
import matplotlib.pyplot as plt


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)


def map_reduce(text):
    words = text.translate(str.maketrans("", "", string.punctuation)).split()

    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    shuffled_values = shuffle_function(mapped_values)

    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)


def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def visualize_top_words(word_counter):
    plt.figure(figsize=(10, 5))
    plt.bar([k for k in word_counter], [word_counter[k]
            for k in word_counter], color='skyblue')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title(f'Top {top_n} Most Frequent Words')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def top(word_count, n):
    return dict(Counter(word_count).most_common(n))


if __name__ == "__main__":
    url = "https://www.gutenberg.org/files/1342/1342-0.txt"
    top_n = 40

    text = fetch_text_from_url(url)
    if not text:
        exit(1)

    total_word_count = top(map_reduce(text), top_n)

    visualize_top_words(total_word_count)

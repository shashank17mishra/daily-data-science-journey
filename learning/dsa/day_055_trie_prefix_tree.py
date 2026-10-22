"""Advanced Trie (Prefix Tree) Implementation with wildcard search, deletion, and auto-complete."""

from typing import Dict, List, Optional


class TrieNode:
    """Node structure for Trie (Prefix Tree)."""

    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False
        self.prefix_count: int = 0


class Trie:
    """Advanced Trie supporting insert, delete, pattern matching, and auto-complete."""

    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        """Insert a word into the Trie.

        Args:
            word: The string to insert.
        """
        if not word:
            return

        node = self.root
        node.prefix_count += 1

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.prefix_count += 1

        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Check if an exact word exists in the Trie.

        Args:
            word: The string to search for.

        Returns:
            True if word exists and is marked as end of word, False otherwise.
        """
        node = self._find_node(word)
        return node is not None and node.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """Check if any word in the Trie starts with the given prefix.

        Args:
            prefix: The prefix string to search for.

        Returns:
            True if prefix exists in the Trie, False otherwise.
        """
        node = self._find_node(prefix)
        return node is not None

    def delete(self, word: str) -> bool:
        """Delete a word from the Trie and prune unused nodes.

        Args:
            word: The word to delete.

        Returns:
            True if word was found and deleted, False otherwise.
        """
        if not self.search(word):
            return False

        def _delete_helper(curr_node: TrieNode, word_idx: int) -> bool:
            if word_idx == len(word):
                curr_node.is_end_of_word = False
                curr_node.prefix_count -= 1
                return len(curr_node.children) == 0

            char = word[word_idx]
            child_node = curr_node.children[char]
            should_delete_child = _delete_helper(child_node, word_idx + 1)

            curr_node.prefix_count -= 1

            if should_delete_child:
                del curr_node.children[char]
                return (not curr_node.is_end_of_word) and (len(curr_node.children) == 0)

            return False

        _delete_helper(self.root, 0)
        return True

    def count_words_with_prefix(self, prefix: str) -> int:
        """Count total words that start with the given prefix.

        Args:
            prefix: The prefix string.

        Returns:
            Integer count of words sharing the prefix.
        """
        if not prefix:
            return self.root.prefix_count

        node = self._find_node(prefix)
        return node.prefix_count if node else 0

    def autocomplete(self, prefix: str, limit: Optional[int] = None) -> List[str]:
        """Find all words in the Trie starting with given prefix up to optional limit.

        Args:
            prefix: Prefix to match.
            limit: Maximum number of suggestions to return.

        Returns:
            List of matching words sorted lexicographically.
        """
        node = self._find_node(prefix)
        if not node:
            return []

        results: List[str] = []

        def _dfs(curr: TrieNode, current_path: List[str]) -> None:
            if limit is not None and len(results) >= limit:
                return

            if curr.is_end_of_word:
                results.append("".join(current_path))

            for char in sorted(curr.children.keys()):
                if limit is not None and len(results) >= limit:
                    break
                _dfs(curr.children[char], current_path + [char])

        _dfs(node, list(prefix))
        return results

    def search_pattern(self, pattern: str) -> List[str]:
        """Search words matching a wildcard pattern where '.' matches any character.

        Args:
            pattern: Pattern string (e.g., 'a.p.e' or 'cat').

        Returns:
            List of matching words in the Trie.
        """
        results: List[str] = []

        def _dfs(node: TrieNode, idx: int, current_path: List[str]) -> None:
            if idx == len(pattern):
                if node.is_end_of_word:
                    results.append("".join(current_path))
                return

            char = pattern[idx]
            if char == ".":
                for next_char in sorted(node.children.keys()):
                    _dfs(node.children[next_char], idx + 1, current_path + [next_char])
            elif char in node.children:
                _dfs(node.children[char], idx + 1, current_path + [char])

        _dfs(self.root, 0, [])
        return results

    def _find_node(self, prefix: str) -> Optional[TrieNode]:
        """Internal helper to navigate to the node corresponding to prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

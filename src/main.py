from textnode import TextNode
from textnode import TextType

def main():
    TextNodeDemo = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    
    print (TextNodeDemo)
    
if __name__ == "__main__":
    main()
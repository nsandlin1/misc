// Name: Novi Sandlin
// Date: 7/15/22
// Course Number and Section: CSC 220 001
// Quarter: Summer 2022
// Assignment #: P2

public class LL {
    // determine whether a linked list is empty
    public static boolean isEmpty(Node h) {
        return h == null;
    }

    // display the contents of a linked list
    public static void display(Node h) {
        if (h == null) {
            System.out.println("List is Empty.");
        }

        Node curr = h;

        while (curr != null) {
            System.out.print(curr.getData() + " ");
            curr = curr.getLink();
        }

        System.out.println();
    }

    // create a linked list with values 1, 2, 3 ... k.
    public static Node generate(int k) {
        if (k == 0) {
            return null;
        }
        if (k < 0) {
            System.out.println("Cannot generate a negatively lengthed list.");
            return null;
        }

        Node head = new Node();

        Node curr = head;
        curr.setData(1);
        // iterate through i values and generate respective node
        for (int i=2; i<=k; i++) {
            curr.setLink(new Node());
            curr = curr.getLink();
            curr.setData(i);
        }

        return head;
    }

    // receives head and returns length
    public static int length(Node h) {
        // redundant?
        if (h == null) { 
            return 0;
        }

        Node curr = h;
        int i = 0;

        // iterate through while updating i counter
        while (curr != null) {
            i++;
            curr = curr.getLink();
        }

        return i;
    }

    public static Node generateRandom(int x) {
        // edge cases
        if (x == 0) {
            return null;
        }
        if (x < 0) {
            System.out.println("Cannot generate a negative lengthed list.");
            return null;
        }

        // initial node
        Node head = new Node();
        head.setData((int) (Math.random()*100));

        // iterate through length and generate nodes
        Node curr = head;
        for (int i=1; i<x; i++) {
            curr.setLink(new Node());
            curr = curr.getLink();
            curr.setData((int) (Math.random()*100));
        }

        return head;
    }

    public static Node insertFront(Node h, int x) {
        Node newNode = new Node();
        newNode.setData(x);
        newNode.setLink(h);

        return newNode;
    }

    public static Node insertEnd(Node h, int x) {

        Node newNode = new Node();
        newNode.setData(x);

        if (h == null) {
            return newNode;
        }

        // iterate through to get last node
        Node curr = h;
        while (curr.getLink() != null) {
            curr = curr.getLink();
        }

        // add new node to link of last node
        curr.setLink(newNode);

        return h;
    }

    // deletes index i in list
    public static Node delete(Node h, int i) {
        if (h == null) {
            return null;
        }
        if (i < 0) {
            System.out.println("Index out of range.");
            return h;
        }
        if (i == 0) {
            if (h.getLink() != null) {
                h = h.getLink();
                return h;
            } else {
                return null;
            }
        }

        int j = 1;
        Node curr = h;

        // iterate through to get node before deleting index
        while (j < i) {
            if (curr.getLink() == null) {
                System.out.println("Index out of range.");
                return h;
            }

            curr = curr.getLink();
            j++;
        }

        // delete, if out of range return h unedited
        try {
            curr.setLink(curr.getLink().getLink());
            return h;
        } catch (Exception e) {
            System.out.println("Index out of range.");
            return h;
        }
    }

    // deletes integer x in list
    public static Node delete2(Node n, int x) {
        // empty list
        if (n == null) {
            return null;
        } 
        // list with one integer
        else if (n.getData() == x) {
            return(n.getLink());
        }
        else {
            Node curr = n;

            while (curr.getLink() != null) {
                if (curr.getLink().getData() == x) {
                    curr.setLink(curr.getLink().getLink());
                    break;
                }
                curr = curr.getLink();
            }
        }
        return n;
    }

    public static Node sortedMerge(Node h1, Node h2) {
        Node aux = null;
        if (h1 == null) {
            return h2;
        }
        if (h2 == null) {
            return h1;
        }
        if (h1.getData() < h2.getData()) {
            aux = h1;
            aux.setLink(sortedMerge(h1.getLink(), h2));
        } else {
            aux = h2;
            aux.setLink(sortedMerge(h1, h2.getLink()));
        }
        return aux;
    }

}

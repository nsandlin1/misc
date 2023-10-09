// Name: Novi Sandlin
// Date: 7/25/22
// Course Number and Section: CSC 220 001
// Quarter: Summer 2022
// Assignment #: P2

import java.io.FileReader;
import java.io.FileWriter;
import java.util.Scanner;
import java.io.File;

public class BST {
    /* Receives the root of a BST and returns true if and only
    if the tree is empty */
    public static boolean isEmpty(TNode n) {
        return (n == null);
    }

    /* Receives the root of a BST and displays its contents in
    in-order recursively */
    public static void inOrderDisplay(TNode n) {
        if (n != null) {
            inOrderDisplay(n.getLeftLink());
            System.out.print(n.getData() + " ");
            inOrderDisplay(n.getRightLink());
        }
    }

    /* Receives the root of a BST and displays its contents in
    pre-order recursively */
    public static void preOrderDisplay(TNode n) {
        if (n != null) {
            System.out.print(n.getData() + " ");
            preOrderDisplay(n.getLeftLink());
            preOrderDisplay(n.getRightLink());
        }
    }

    /* Receives the root of a BST and displays its contents in
    post-order recursively */ 
    public static void postOrderDisplay(TNode n) {
        if (n != null) {
            postOrderDisplay(n.getLeftLink());
            postOrderDisplay(n.getRightLink());
            System.out.print(n.getData() + " ");
        }
    }

    /* Receives the root of a BST and returns the smallest
    value. If given an empty tree, either return a "null" value
    or throw an exception. */ 
    public static int getMin(TNode n) throws NullPointerException {
        if (n == null) {
            throw new NullPointerException("Given tree is null.");
        }
        if (n.getLeftLink() == null) {
            return n.getData();
        }
        return getMin(n.getLeftLink());
    }

    /* Receives the root of a BST and returns the largest
    value. If given an empty tree, either return a "null" value
    or throw an exception. */ 
    public static int getMax(TNode n) throws NullPointerException {
        if (n == null) {
            throw new NullPointerException("Given tree is null.");
        }
        if (n.getRightLink() == null) {
            return n.getData();
        }
        return getMax(n.getRightLink());
    }

    /* Receives the root of a BST and an integer. Creates a new
    tree node containing data value x and inserts it correctly
    into the tree. Return the root of the adjusted tree. If a
    duplicate value is attempted, then either give and handle
    an error or return the root of the original tree
    unadjusted. */ 
    public static TNode insert(TNode n, int x) {
        if (n == null) {
            n = new TNode(x);
            return n;
        }

        if (x < n.getData()) {
            insertHelper(n.getLeftLink(), n, x);
        } else if (x > n.getData()) {
            insertHelper(n.getRightLink(), n, x);
        }

        return n;
    }

    private static void insertHelper(TNode n, TNode parent, int x) {
        // if found null node
        if (n == null) {
            if (x < parent.getData()) {
                parent.setLeftLink(new TNode(x));
            }
            if (x > parent.getData()) {
                parent.setRightLink(new TNode(x));
            }
            return;
        }
        // if x already in tree
        if (n.getData() == x) {
            return;
        }

        if (x < n.getData()) {
            insertHelper(n.getLeftLink(), n, x);
        } else if (x > n.getData()) {
            insertHelper(n.getRightLink(), n, x);
        }
    }

    /* Receives the root of a BST and an integer x. Deletes the
    node that contains data value x, if it exists. Then adjusts
    remaining nodes so that the tree remains a BST according to
    the recursive algorithm given in class. Returns the root of
    the finished tree. May call the method getMin. */
    // utilizes getMin()
    public static TNode delete(TNode root, int x) throws Exception {
        if (root == null) {
            throw new Exception("Item not found.");
        } else if (x > root.getData()) {
            root.setRightLink(delete(root.getRightLink(), x));
        } else if (x < root.getData()) {
            root.setLeftLink(delete(root.getLeftLink(), x));
        } else {
            if (root.getLeftLink() == null && root.getRightLink() == null) {
                return null;
            }
            if (root.getLeftLink() == null) {
                return root.getRightLink();
            }
            if (root.getRightLink() == null) {
                return root.getLeftLink();
            }
            root.setData(getMin(root.getRightLink()));
            root.setRightLink(delete(root.getRightLink(), root.getData()));
        }
        return root;
    }

    /* Receives the root of a BST and returns the number of
    nodes in the tree. */   
    public static int nodeCount(TNode n) {
        if (n == null) {
         return 0;
        }
        if (n.getLeftLink() == null && n.getRightLink() == null) {
            return 1;
        }
        return 1 + nodeCount(n.getLeftLink()) + nodeCount(n.getRightLink());
    }

    /* Receives an integer k. Creates a BST containing k random
    integers from 0-100. Returns the root of the tree created.
    Returns null if a non-positive integer is received. May
    call the method insert. */
    public static TNode generateRandom(int k) {
        if (k <= 0) {
            return null;
        }

        TNode head = new TNode((int) (Math.random()*100));

        for (int i=1; i<k; i++) {
            int num = (int) (Math.random() * 100) + 1;
            insert(head, num);
        }

        return head;
    }

    /* Receives a string representing a file name. Creates a
    BST containing the integers in the file in the order they
    are listed. The file format will have integers separated by
    spaces. Returns the root of the tree created. Returns null
    or throws an exception if reading unsuccessful. May call
    the method insert. */
    public static TNode treeRead(String fileName) throws Exception {
        TNode head = null;
        int numNums = 0;
        FileReader infile = null;
        
        try {
            try {
                infile = new FileReader(fileName);
            } catch (Exception e) {
                throw new Exception("File does not exist.");
            }
            
            Scanner scn = new Scanner(infile);

            // see if file empyt (does not check for NEWLINE characters)
            File file = new File(fileName);
            if (file.length() == 0) {
                scn.close();
                throw new Exception("Input file is empty or does not exist.");
            }

            while (scn.hasNextInt()) {
                int i = scn.nextInt();
                head = insert(head, i);
                numNums++;
            }

            // if NEWLINE present
            if (numNums == 0) {
                scn.close();
                throw new Exception("File contains no Double type.");
            }
            
            // check for none-double type
            if (scn.hasNext() == true) {
                scn.close();
                throw new Exception("File contains none Double type.");
            }

            scn.close();
            return head;

        } catch (Exception e) {
            throw e;
        }
    }

    /* Receives a string representing a file name and the root
    of a BST. Writes the integers contained in the tree in preorder to the file. */
    public static void treeWrite(TNode root, String fileName) throws Exception {
        try {
            if (root == null) {
                throw new Exception("root given is null value");
            }

            FileWriter outfile = new FileWriter(fileName);
            
            treeWriteHelper(root, fileName, outfile);

            outfile.close();

        } catch (Exception e) {
            throw e;
        }
    }

    private static void treeWriteHelper(TNode n, String fileName, FileWriter outFile) throws Exception {
        try {
            if (n != null) {
                outFile.write(Integer.toString(n.getData()) + " ");
                treeWriteHelper(n.getLeftLink(), fileName, outFile);
                treeWriteHelper(n.getRightLink(), fileName, outFile);
            }
        } catch (Exception e) {
            throw e;
        }
    }

    /* Code given to display a tree to screen. */
    public static void displayTree2(TNode root, int space) {
        if (root != null) {
            space += 10;
            displayTree2(root.getRightLink(), space);
            System.out.println();

            for (int i = 10; i<space; i++)
                System.out.print(" ");

            System.out.print(root.getData() + "\n");

            displayTree2(root.getLeftLink(), space);
        }
    }
}

import xml.dom.minidom

'''
Load XML doc and operate on it in memory'''

def main():
    xfile = '/Users/sbommireddy/Documents/python/assignments/dq/python/samplexml.xml'
    doc = xml.dom.minidom.parse(xfile)

    print(doc.nodeName)
    print(doc.firstChild.tagName)

    # get a list of xml tags from the doc ad print eachone.
    print("*"*50)
    name = doc.getElementsByTagName("skill")
    print("%d skills" %name.length)
    for n in name:
        print(n.getAttribute('name'))

    # Create a new xml tag.
    newskill = doc.createElement("skill")
    newskill.setAttribute("name","Docker")
    doc.firstChild.appendChild(newskill)

    print("*"*50)
    name = doc.getElementsByTagName("skill")
    print("%d skills" %name.length)
    for n in name:
        print(n.getAttribute('name'))

if __name__ == '__main__':
    main()

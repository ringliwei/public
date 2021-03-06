# 泛型

## Table of Contents

- [泛型](#%e6%b3%9b%e5%9e%8b)
  - [Table of Contents](#table-of-contents)
  - [结论](#%e7%bb%93%e8%ae%ba)
  - [C# 代码](#c-%e4%bb%a3%e7%a0%81)
  - [Java 代码](#java-%e4%bb%a3%e7%a0%81)
  - [C#协变与逆变](#c%e5%8d%8f%e5%8f%98%e4%b8%8e%e9%80%86%e5%8f%98)
    - [背景知识：协变和逆变](#%e8%83%8c%e6%99%af%e7%9f%a5%e8%af%86%e5%8d%8f%e5%8f%98%e5%92%8c%e9%80%86%e5%8f%98)
    - [.NET 4.0引入的泛型协变、逆变性](#net-40%e5%bc%95%e5%85%a5%e7%9a%84%e6%b3%9b%e5%9e%8b%e5%8d%8f%e5%8f%98%e9%80%86%e5%8f%98%e6%80%a7)
    - [总结](#%e6%80%bb%e7%bb%93)
  - [Kotlin](#kotlin)
    - [型变](#%e5%9e%8b%e5%8f%98)
    - [声明处型变](#%e5%a3%b0%e6%98%8e%e5%a4%84%e5%9e%8b%e5%8f%98)
    - [类型投影](#%e7%b1%bb%e5%9e%8b%e6%8a%95%e5%bd%b1)
    - [星投影](#%e6%98%9f%e6%8a%95%e5%bd%b1)
    - [泛型函数](#%e6%b3%9b%e5%9e%8b%e5%87%bd%e6%95%b0)
    - [类型擦除](#%e7%b1%bb%e5%9e%8b%e6%93%a6%e9%99%a4)
  - [Scala](#scala)

## 结论

1. C#泛型的in, out关键字与Java中的?通配符解决了：如果B是A的子类，则C`<A>`与 C`<B>` 是否具有子类型化的关系。
2. `Object[] a = new SubClass[10];`没有编译时错误，如果有，那么各种泛型数据结构将不能实现。
3. C#中in, out关键字用于接口和委托，在定义泛型时就决定了逆变协变关系。Java则是在使用时通过指定super，extends关键字结合通配符`{?}`来决定逆变协变关系。
4. 记住一点：C`<A>`与 C`<B>`之间是否具有协变或者逆变的关系。
5. C# is declaration-site variance, java is use-site variance. C#是声明处型变，Java是使用处型变。
    > kotlin兼具声明处型变及使用处型变
6. C#泛型约束(constraints-on-type-parameters)通过where关键字指定。Java中则通过extends, super关键字指定类型边界(bound-on-type-parameters)。
7. 助记表

| 生产者     | 消费者   |
|---------|-------|
| 返回值     | 参数    |
| PE      | CS    |
| extends | super |
| OUT     | IN    |
| 协变      | 逆变    |

## C# 代码

```C#
public class Person { }

public class Student : Person { }

public class LittleStudent : Student { }

public delegate void Action<in T>(T obj);

public void test()
{
    List<Student> students = new List<Student>();

    Action<Person> pAction = (item) => { };
    Action<Student> sAction = p;
    Action<LittleStudent> lAction = (item) => { };

    // 正确：Action<Person>可以安全的转换为Action<Student>。
    // Action<in T> 对T具有逆变安全性。
    students.ForEach(pAction);

    // 正确
    students.ForEach(sAction);

    // 编译时错误，原因如下：
    // 假定可以通过编译：lAction接受的是LittleStudent，而现在传入的是Student.
    // 显然Student不能安全的转换为LittleStudent
    students.ForEach(lAction);
}

```

## Java 代码

```java

public class Person { }

public class Student extends Person { }

public class LittleStudent extends Student { }

//////////////////// 定义END ///////////////////////////

public void test() {
    List<Student> students = new ArrayList<Student>();
    List<? extends Student> y = students;

    Consumer<Person> p = (item) -> {};
    Consumer<? super Student> c = p;

    students.forEach(p);
    students.forEach(c);

    y.forEach(c);
    y.forEach(p);

    List<? super Student> superStudents = new ArrayList<Person>();

    // 编译时错误
    superStudents.forEach(p);
    // 编译时错误
    superStudents.forEach(c);

    Consumer<Object> o = (item)->{};
    // 正确
    superStudents.forEach(o);
}

```

## C#协变与逆变

[.NET 4.0中的泛型协变和反变](https://www.cnblogs.com/Ninputer/archive/2008/11/22/generic_covariant.html)

[Covariance and Contravariance](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/covariance-contravariance/)

> 协变<===>逆变

随Visual Studio 2010 CTP亮相的C#4和VB10，虽然在支持语言新特性方面走了相当不一样的两条路：C#着重增加后期绑定和与动态语言相容的若干特性，VB10着重简化语言和提高抽象能力；但是两者都增加了一项功能：泛型类型的协变（covariant）和逆变（contravariant）。许多人对其了解可能仅限于增加的in/out关键字，而对其诸多特性有所不知。下面我们就对此进行一些详细的解释，帮助大家正确使用该特性。

### 背景知识：协变和逆变

很多人可能不不能很好地理解这些来自于物理和数学的名词。我们无需去了解他们的数学定义，但是至少应该能分清协变和逆变。实际上这个词来源于类型和类型之间的绑定。我们从数组开始理解。数组其实就是一种和具体类型之间发生绑定的类型。数组类型Int32[]就对应于Int32这个原本的类型。任何类型T都有其对应的数组类型T[]。那么我们的问题就来了，如果两个类型T和U之间存在一种安全的隐式转换，那么对应的数组类型T[]和U[]之间是否也存在这种转换呢？这就牵扯到了将原本类型上存在的类型转换映射到他们的数组类型上的能力，这种能力就称为“`可变性（Variance）`”。在.NET世界中，唯一允许可变性的类型转换就是由继承关系带来的“子类引用->父类引用”转换。举个例子，就是String类型继承自Object类型，所以任何String的引用都可以安全地转换为Object引用。我们发现String[]数组类型的引用也继承了这种转换能力，它可以转换成Object[]数组类型的引用，数组这种与原始类型转换方向相同的可变性就称作`协变（covariant）`。

由于数组不支持逆变性，我们无法用数组的例子来解释逆变性，所以我们现在就来看看泛型接口和泛型委托的`可变性`。假设有这样两个类型：TSub是TParent的子类，显然TSub型引用是可以安全转换为TParent型引用的。如果一个泛型接口`IFoo<T>`，`IFoo<TSub>`可以转换为`IFoo<TParent>`的话，我们称这个过程为`协变`，而且说这个泛型接口支持对T的协变。而如果一个泛型接口`IBar<T>`，`IBar<TParent>`可以转换为`T<TSub>`的话，我们称这个过程为`逆变（contravariant）`，而且说这个`接口支持对T的逆变`。因此很好理解，如果一个可变性和子类到父类转换的方向一样，就称作`协变`；而如果和子类到父类的转换方向相反，就叫`逆变性`。你记住了吗？

### .NET 4.0引入的泛型协变、逆变性

刚才我们讲解概念的时候已经用了泛型接口的协变和逆变，但在.NET 4.0之前，无论C#还是VB里都不支持泛型的这种可变性。不过它们都支持委托参数类型的协变和逆变。由于委托参数类型的可变性理解起来抽象度较高，所以我们这里不准备讨论。已经完全能够理解这些概念的读者自己想必能够自己去理解委托参数类型的可变性。在.NET 4.0之前为什么不允许`IFoo<T>`进行协变或逆变呢？因为对接口来讲，T这个类型参数既可以用于方法参数，也可以用于方法返回值。设想这样的接口

```vb
Interface IFoo(Of T)

    Sub Method1(ByVal param As T)

    Function Method2() As T

End Interface
```

```C#
interface IFoo<T>
{

    void Method1(T param);

    T Method2();

}
```

如果我们允许协变，从`IFoo<TSub>`到`IFoo<TParent>`转换，那么`IFoo.Method1(TSub)`就会变成`IFoo.Method1(TParent)`。我们都知道TParent是不能安全转换成TSub的，所以Method1这个方法就会变得不安全。同样，如果我们允许逆变`IFoo<TParent>`到`IFoo<TSub>`，则`TParent IFoo.Method2()`方法就会变成`TSub IFoo.Method2()`，原本返回的TParent引用未必能够转换成TSub的引用，Method2的调用将是不安全的。有此可见，在没有额外机制的限制下，接口进行协变或逆变都是类型不安全的。.NET 4.0改进了什么呢？它允许在类型参数的声明时增加一个额外的描述，以确定这个类型参数的使用范围。我们看到，如果一个类型参数仅仅能用于函数的返回值，那么这个类型参数就对协变相容。而相反，一个类型参数如果仅能用于方法参数，那么这个类型参数就对逆变相容。如下所示：

```C#
Interface ICo(Of Out T)

    Function Method() As T

End Interface
```

```vb
Interface IContra(Of In T)

    Sub Method(ByVal param As T)

End Interface
```

```C#
interface ICo<out T>
{

    T Method();

}
```

```C#
interface IContra<in T>
{

    void Method(T param);

}
```

可以看到C#4和VB10都提供了大同小异的语法，用Out来描述仅能作为返回值的类型参数，用In来描述仅能作为方法参数的类型参数。一个接口可以带多个类型参数，这些参数可以既有In也有Out，因此我们不能简单地说一个接口支持协变还是逆变，只能说一个接口对某个具体的类型参数支持协变或逆变。比如若有`IBar<in T1, out T2>`这样的接口，则它对T1支持逆变而对T2支持协变。举个例子来说，`IBar<object, string>`能够转换成`IBar<string, object>`，这里既有协变又有逆变。

在.NET Framework中，许多接口都仅仅将类型参数用于参数或返回值。为了使用方便，在.NET Framework 4.0里这些接口将重新声明为允许协变或逆变的版本。例如`IComparable<T>`就可以重新声明成`IComparable<in T>`，而`IEnumerable<T>`则可以重新声明为`IEnumerable<out T>`。不过某些接口`IList<T>`是不能声明为in或out的，因此也就无法支持协变或逆变。

下面提起几个泛型协变和逆变容易忽略的注意事项：

1. 仅有泛型接口和泛型委托支持对类型参数的可变性，泛型类或泛型方法是不支持的。

2. 值类型不参与协变或逆变，`IFoo<int>`永远无法变成`IFoo<object>`，不管有无声明out。因为.NET泛型，每个值类型会生成专属的封闭构造类型，与引用类型版本不兼容。

3. 声明属性时要注意，可读写的属性会将类型同时用于参数和返回值。因此只有只读属性才允许使用out类型参数，只写属性能够使用in参数。

协变和逆变的相互作用
这是一个相当有趣的话题，我们先来看一个例子：

```vb
Interface IFoo(Of In T)
End Interface
```

```vb
Interface IBar(Of In T)

    Sub Test(ByVal foo As IFoo(Of T)) '对吗？

End Interface
```

```c#
interface IFoo<in T>
{
}
```

```c#
interface IBar<in T>
{

    void Test(IFoo<T> foo); //对吗？

}
```

你能看出上述代码有什么问题吗？我声明了in T，然后将他用于方法的参数了，一切正常。但出乎你意料的是，这段代码是无法编译通过的！反而是这样的代码通过了编译：

```vb
Interface IFoo(Of In T)
End Interface
```

```vb
Interface IBar(Of Out T)

    Sub Test(ByVal foo As IFoo(Of T))

End Interface
```

```C#
interface IFoo<in T>
{
}
```

```C#
interface IBar<out T>
{
    void Test(IFoo<T> foo);
}
```

什么？明明是out参数，我们却要将其用于方法的参数才合法？初看起来的确会有一些惊奇。我们需要费一些周折来理解这个问题。现在我们考虑`IBar<string>`，它应该能够协变成`IBar<object>`，因为string是object的子类。因此`IBar.Test(IFoo<string>)`也就协变成了`IBar.Test(IFoo<object>)`。当我们调用这个协变后方法时，将会传入一个`IFoo<object>`作为参数。想一想，这个方法是从`IBar.Test(IFoo<string>)`协变来的，所以参数`IFoo<object>`必须能够变成`IFoo<string>`才能满足原函数的需要。这里对`IFoo<object>`的要求是它能够逆变成`IFoo<string>`！而不是协变。也就是说，如果一个接口需要对T协变，那么这个接口所有方法的参数类型必须支持对T的逆变。同理我们也可以看出，如果接口要支持对T逆变，那么接口中方法的参数类型都必须支持对T协变才行。这就是方法参数的协变-逆变互换原则。所以，我们并不能简单地说out参数只能用于返回值，它确实只能直接用于声明返回值类型，但是只要一个支持逆变的类型协助，out类型参数就也可以用于参数类型！换句话说，in参数除了直接声明方法参数之外，也仅能借助支持协变的类型才能用于方法参数，仅支持对T逆变的类型作为方法参数也是不允许的。要想深刻理解这一概念，第一次看可能会有点绕，建议有条件的情况下多进行一些实验。

刚才提到了方法参数上协变和逆变的相互影响。那么方法的返回值会不会有同样的问题呢？我们看如下代码：

```vb
Interface IFooCo(Of Out T)
End Interface
```

```vb
Interface IFooContra(Of In T)

End Interface
```

```vb
Interface IBar(Of Out T1, In T2)

    Function Test1() As IFooCo(Of T1)

    Function Test2() As IFooContra(Of T2)

End Interface
```

```C#
interface IFooCo<out T>
{

}
```

```C#
interface IFooContra<in T>
{

}
```

```C#
interface IBar<out T1, in T2>
{
    IFooCo<T1> Test1();
    IFooContra<T2> Test2();
}
```

我们看到和刚刚正好相反，如果一个接口需要对T进行协变或逆变，那么这个接口所有方法的返回值类型必须支持对T同样方向的协变或逆变。这就是方法返回值的协变-逆变一致原则。也就是说，即使in参数也可以用于方法的返回值类型，只要借助一个可以逆变的类型作为桥梁即可。如果对这个过程还不是特别清楚，建议也是写一些代码来进行实验。至此我们发现协变和逆变有许多有趣的特性，以至于在代码里in和out都不像他们字面意思那么好理解。当你看到in参数出现在返回值类型，out参数出现在参数类型时，千万别晕倒，用本文的知识即可破解其中奥妙。

### 总结

经过本文的讲解，大家应该已经初步了解的协变和逆变的含义，能够分清协变、逆变的过程。我们还讨论了`.NET 4.0`支持泛型接口、委托的协变和逆变的新功能和新语法。最后我们还套了论的协变、逆变与函数参数、返回值的相互作用原理，以及由此产生的奇妙写法。我希望大家看了我的文章后，能够将这些知识用于泛型程序设计当中, 正确运用.NET 4.0的新增功能。祝大家使用愉快！

> 1. 如果接口要支持对T逆变，那么接口中方法的参数类型都必须支持对T协变才行。这就是`方法参数`的**协变-逆变互换原则**。
> 2. 如果一个接口需要支持对T进行协变或逆变，那么这个接口所有方法的返回值类型必须支持对T同样方向的协变或逆变。这就是`方法返回值`的**协变-逆变一致原则**

## Kotlin

[英文文档](http://kotlinlang.org/docs/reference/generics.html)

[中文文档](https://www.kotlincn.net/docs/reference/generics.html)

与 Java 类似，Kotlin 中的类也可以有类型参数：

```kotlin
class Box<T>(t: T) {
    var value = t
}
```

一般来说，要创建这样类的实例，我们需要提供类型参数：

```kotlin
val box: Box<Int> = Box<Int>(1)
```

但是如果类型参数可以推断出来，例如从构造函数的参数或者从其他途径，允许省略类型参数：

```kotlin
val box = Box(1) // 1 具有类型 Int，所以编译器知道我们说的是 Box<Int>。
```

### 型变

Java 类型系统中最棘手的部分之一是通配符类型（参见 [Java Generics FAQ](http://www.angelikalanger.com/GenericsFAQ/JavaGenericsFAQ.html)）。 而 Kotlin 中没有。 相反，它有两个其他的东西：声明处型变（`declaration-site variance`）与类型投影（`type projections`）。

首先，让我们思考为什么 Java 需要那些神秘的通配符。在 《Effective Java》第三版 解释了该问题——第 31 条：利用有限制通配符来提升 API 的灵活性。 首先，Java 中的泛型是不型变的，这意味着 `List<String>` 并不是 `List<Object>` 的子类型。 为什么这样？ 如果 List 不是不型变的，它就没比 Java 的数组好到哪去，因为如下代码会通过编译然后导致运行时异常：

```java
// Java
List<String> strs = new ArrayList<String>();
List<Object> objs = strs; // ！！！即将来临的问题的原因就在这里。Java 禁止这样！
objs.add(1); // 这里我们把一个整数放入一个字符串列表
String s = strs.get(0); // ！！！ ClassCastException：无法将整数转换为字符串
```

因此，Java 禁止这样的事情以保证运行时的安全。但这样会有一些影响。例如，考虑 Collection 接口中的 addAll() 方法。该方法的签名应该是什么？直觉上，我们会这样：

```java
// Java
interface Collection<E> …… {
  void addAll(Collection<E> items);
}
```

但随后，我们将无法做到以下简单的事情（这是完全安全）：

```java
// Java
void copyAll(Collection<Object> to, Collection<String> from) {
  to.addAll(from);
  // ！！！对于这种简单声明的 addAll 将不能编译：
  // Collection<String> 不是 Collection<Object> 的子类型
}
```

（在 Java 中，我们艰难地学到了这个教训，参见《Effective Java》第三版，第 28 条：列表优先于数组）

这就是为什么 addAll() 的实际签名是以下这样：

```java
// Java
interface Collection<E> …… {
  void addAll(Collection<? extends E> items);
}
```

通配符类型参数`? extends E`表示此方法接受 E 或者 E 的 一些子类型对象的集合，而不只是 E 自身。 这意味着我们可以安全地从其中（该集合中的元素是 E 的子类的实例）读取 E，但不能写入， 因为我们不知道什么对象符合那个未知的 E 的子类型。 反过来，该限制可以让`Collection<String>`表示为`Collection<? extends Object>`的子类型。 简而言之，带 extends 限定（上界）的通配符类型使得类型是协变的（covariant）。

理解为什么这个技巧能够工作的关键相当简单：如果只能从集合中获取项目，那么使用 String 的集合， 并且从其中读取 Object 也没问题 。反过来，如果只能向集合中 放入 项目，就可以用 Object 集合并向其中放入 String：在 Java 中有 `List<? super String>` 是 `List<Object>` 的一个超类。

后者称为逆变性（contravariance），并且对于 `List <? super String>` 你只能调用接受 String 作为参数的方法 （例如，你可以调用 `add(String)` 或者 `set(int, String)`），当然如果调用函数返回 `List<T>` 中的 T，你得到的并非一个 String 而是一个 Object。

Joshua Bloch 称那些你只能从中读取的对象为生产者，并称那些你只能写入的对象为消费者。他建议：“为了灵活性最大化，在表示生产者或消费者的输入参数上使用通配符类型”，并提出了以下助记符：

PECS 代表`生产者-Extens`，`消费者-Super`（`Producer-Extends`, `Consumer-Super`）。

注意：如果你使用一个生产者对象，如 `List<? extends Foo>`，在该对象上不允许调用 add() 或 set()。但这并不意味着该对象是不可变的：例如，没有什么阻止你调用 clear()从列表中删除所有项目，因为 clear() 根本无需任何参数。通配符（或其他类型的型变）保证的唯一的事情是类型安全。不可变性完全是另一回事。

### 声明处型变

假设有一个泛型接口 `Source<T>`，该接口中不存在任何以 T 作为参数的方法，只是方法返回 `T` 类型值：

```java
// Java
interface Source<T> {
  T nextT();
}
```

那么，在 `Source <Object>` 类型的变量中存储 `Source <String>` 实例的引用是极为安全的——没有消费者-方法可以调用。但是 Java 并不知道这一点，并且仍然禁止这样操作：

```java
// Java
void demo(Source<String> strs) {
  Source<Object> objects = strs; // ！！！在 Java 中不允许
}
```

为了修正这一点，我们必须声明对象的类型为 `Source<? extends Object>`，这是毫无意义的，因为我们可以像以前一样在该对象上调用所有相同的方法，所以更复杂的类型并没有带来价值。但编译器并不知道。

在 Kotlin 中，有一种方法向编译器解释这种情况。这称为声明处型变：我们可以标注 Source 的类型参数 T 来确保它仅从 `Source<T>` 成员中返回（生产），并从不被消费。 为此，我们提供 out 修饰符：

```kotlin
interface Source<out T> {
    fun nextT(): T
}
```

```kotlin
fun demo(strs: Source<String>) {
    val objects: Source<Any> = strs // 这个没问题，因为 T 是一个 out-参数
}
```

一般原则是：当一个类 C 的类型参数 T 被声明为 out 时，它就只能出现在 C 的成员的输出-位置，但回报是 `C<Base>` 可以安全地作为 `C<Derived>`的超类。

简而言之，他们说类 C 是在参数 T 上是协变的，或者说 T 是一个协变的类型参数。 你可以认为 C 是 T 的生产者，而不是 T 的消费者。

out修饰符称为型变注解，并且由于它在类型参数声明处提供，所以我们讲声明处型变。 这与 Java 的使用处型变相反，其类型用途通配符使得类型协变。

另外除了 out，Kotlin 又补充了一个型变注释：in。它使得一个类型参数逆变：只可以被消费而不可以被生产。逆变类型的一个很好的例子是 Comparable：

```kotlin
interface Comparable<in T> {
    operator fun compareTo(other: T): Int
}
```

```kotlin
fun demo(x: Comparable<Number>) {
    x.compareTo(1.0) // 1.0 拥有类型 Double，它是 Number 的子类型
                    // 因此，我们可以将 x 赋给类型为 Comparable <Double> 的变量
    val y: Comparable<Double> = x // OK！
}
```

我们相信 in 和 out 两词是自解释的（因为它们已经在 C# 中成功使用很长时间了），因此上面提到的助记符不是真正需要的，并且可以将其改写为更高的目标：存在性（The Existential） 转换：消费者 in, 生产者 out

### 类型投影

`使用处型变`：**类型投影**

将类型参数 T 声明为 out 非常方便，并且能避免使用处子类型化的麻烦，但是有些类实际上不能限制为只返回 T！ 一个很好的例子是 Array：

```kotlin
class Array<T>(val size: Int) {
    fun get(index: Int): T { …… }
    fun set(index: Int, value: T) { …… }
}
```

该类在 T 上既不能是协变的也不能是逆变的。这造成了一些不灵活性。考虑下述函数：

```kotlin
fun copy(from: Array<Any>, to: Array<Any>) {
    assert(from.size == to.size)
    for (i in from.indices)
        to[i] = from[i]
}
```

这个函数应该将项目从一个数组复制到另一个数组。让我们尝试在实践中应用它：

```kotlin
val ints: Array<Int> = arrayOf(1, 2, 3)
val any = Array<Any>(3) { "" }
copy(ints, any) //   ^ 其类型为 Array<Int> 但此处期望 Array<Any>
```

这里我们遇到同样熟悉的问题：`Array <T>` 在 T 上是不型变的，因此 `Array <Int>` 和 `Array <Any>` 都不是另一个的子类型。为什么？ 再次重复，因为 copy 可能做坏事，也就是说，例如它可能尝试写一个 String 到 from， 并且如果我们实际上传递一个 Int 的数组，一段时间后将会抛出一个 ClassCastException 异常。

那么，我们唯一要确保的是 copy() 不会做任何坏事。我们想阻止它写到 from，我们可以：

```kotlin
fun copy(from: Array<out Any>, to: Array<Any>) { }
```

这里发生的事情称为**类型投影**：我们说from不仅仅是一个数组，而是一个受限制的（投影的）数组：我们只可以调用返回类型为类型参数 T 的方法，如上，这意味着我们只能调用 get()。这就是我们的使用处型变的用法，并且是对应于 Java 的 `Array<? extends Object>`、 但使用更简单些的方式。

你也可以使用 in 投影一个类型：

​```kotlin
fun fill(dest: Array<in String>, value: String) { }
​```

`Array<in String>` 对应于 Java 的 `Array<? super String>`，也就是说，你可以传递一个 CharSequence 数组或一个 Object 数组给 fill() 函数。

### 星投影

有时你想说，你对类型参数一无所知，但仍然希望以安全的方式使用它。 这里的安全方式是定义泛型类型的这种投影，该泛型类型的每个具体实例化将是该投影的子类型。

Kotlin 为此提供了所谓的星投影语法：

对于 `Foo <out T : TUpper>`，其中 T 是一个具有上界 TUpper 的协变类型参数，`Foo <*>`等价于 `Foo <out TUpper>`。 这意味着当 T 未知时，你可以安全地从 `Foo <*>` 读取 `TUpper` 的值。

对于 `Foo <in T>`，其中 T 是一个逆变类型参数，`Foo <*>` 等价于 `Foo <in Nothing>`。 这意味着当 T 未知时，没有什么可以以安全的方式写入 `Foo <*>`。

对于 `Foo <T : TUpper>`，其中 T 是一个具有上界 `TUpper` 的不型变类型参数，`Foo<*>` 对于读取值时等价于 `Foo<out TUpper>` 而对于写值时等价于 `Foo<in Nothing>`。

如果泛型类型具有多个类型参数，则每个类型参数都可以单独投影。 例如，如果类型被声明为 `interface Function <in T, out U>`，我们可以想象以下星投影：

`Function<*, String>` 表示 `Function<in Nothing, String>`；
`Function<Int, *>` 表示 `Function<Int, out Any?>`；
`Function<*, *>` 表示 `Function<in Nothing, out Any?>`。

注意：星投影非常像 Java 的原始类型，但是安全。

### 泛型函数

不仅类可以有类型参数。函数也可以有。类型参数要放在函数名称之前：

```kotlin
fun <T> singletonList(item: T): List<T> {
}
```

```kotlin
fun <T> T.basicToString(): String { // 扩展函数
}
```

要调用泛型函数，在调用处函数名之后指定类型参数即可：

```kotlin
val l = singletonList<Int>(1)
```

可以省略能够从上下文中推断出来的类型参数，所以以下示例同样适用：

```kotlin
val l = singletonList(1)
```

泛型约束
能够替换给定类型参数的所有可能类型的集合可以由泛型约束限制。

上界
最常见的约束类型是与 Java 的 extends 关键字对应的 上界：

```kotlin
fun <T : Comparable<T>> sort(list: List<T>) {  …… }
```

冒号之后指定的类型是上界：只有 `Comparable<T>` 的子类型可以替代 T。 例如：

```kotlin
sort(listOf(1, 2, 3)) // OK。Int 是 Comparable<Int> 的子类型
sort(listOf(HashMap<Int, String>())) // 错误：HashMap<Int, String> 不是 Comparable<HashMap<Int, String>> 的子类型
```

默认的上界（如果没有声明）是 Any?。在尖括号中只能指定一个上界。 如果同一类型参数需要多个上界，我们需要一个单独的 where-子句：

```kotlin
fun <T> copyWhenGreater(list: List<T>, threshold: T): List<String>
    where T : CharSequence,
          T : Comparable<T> {
    return list.filter { it > threshold }.map { it.toString() }
}
```

所传递的类型必须同时满足 where 子句的所有条件。在上述示例中，类型 T 必须既实现了 CharSequence 也实现了 Comparable。

### 类型擦除

Kotlin 为泛型声明用法执行的类型安全检测仅在编译期进行。 运行时泛型类型的实例不保留关于其类型实参的任何信息。 其类型信息称为被擦除。例如，`Foo<Bar>` 与 `Foo<Baz?>` 的实例都会被擦除为 `Foo<*>`。

因此，并没有通用的方法在运行时检测一个泛型类型的实例是否通过指定类型参数所创建 ，并且编译器禁止这种 is 检测。

类型转换为带有具体类型参数的泛型类型，如 `foo as List<String>` 无法在运行时检测。 当高级程序逻辑隐含了类型转换的类型安全而无法直接通过编译器推断时， 可以使用这种非受检类型转换。编译器会对非受检类型转换发出警告，并且在运行时只对非泛型部分检测（相当于 `foo as List<*>`）。

泛型函数调用的类型参数也同样只在编译期检测。在函数体内部， 类型参数不能用于类型检测，并且类型转换为类型参数`（foo as T）`也是非受检的。然而， 内联函数的具体化的类型参数会由调用处内联函数体中的类型实参所代入，因此可以用于类型检测与转换， 与上述泛型类型的实例具有相同限制。

## Scala

[型变](https://docs.scala-lang.org/zh-cn/tour/variances.html)

型变是复杂类型的子类型关系与其组件类型的子类型关系的相关性。 Scala支持 泛型类 的类型参数的型变注释，允许它们是协变的，逆变的，或在没有使用注释的情况下是不变的。 在类型系统中使用型变允许我们在复杂类型之间建立直观的连接，而缺乏型变则会限制类抽象的重用性。

```scala
class Foo[+A] // A covariant class
class Bar[-A] // A contravariant class
class Baz[A]  // An invariant class
```

使用注释 +A，可以使一个泛型类的类型参数 A 成为协变。 对于某些类 class List[+A]，使 A 成为协变意味着对于两种类型 A 和 B，如果 A 是 B 的子类型，那么 List[A] 就是 List[B] 的子类型。 这允许我们使用泛型来创建非常有用和直观的子类型关系。
